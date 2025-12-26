import collections
import csv
import dataclasses
import datetime
import io
import itertools
import json
import logging
import os
import random
import typing
import uuid

import faker
from google.cloud import storage
import numpy as np

fake = faker.Faker()
# final datasets
orders = list()
users = list()
order_items = list()
events = list()
inventory_items = list()


# read from local csv and return products
def generate_products() -> typing.List[dict]:
  product_brand_dict = {}  # products partitioned by brand - unused
  product_category_dict = {}  # product partitioned by cateogry - unused
  gender_category_dict = (
      {}
  )  # products partitioned by gender and category - unused
  product_id_dict = {}  # products to generate events table - unused
  product_gender_dict = {}  # product partitioned by gender
  product_by_id_dict = {}  # products partitioned by product ID

  products = collections.defaultdict(list)
  with open(
      f"{os.environ['SOURCE_DIR']}/products.csv", encoding="utf-8"
  ) as productcsv:
    csv_reader = csv.DictReader(productcsv)
    for rows in csv_reader:
      for k, v in rows.items():
        products[k].append(v)

  product_id = products["id"]
  brands = products["brand"]
  name = products["name"]
  cost = products["cost"]
  category = products["category"]
  department = products["department"]
  sku = products["sku"]
  retail_price = products["retail_price"]
  distribution_center_id = products["distribution_center_id"]
  for _ in range(len(brands)):
    product_brand_dict[brands[_]] = []
    product_category_dict[category[_]] = []
    product_id_dict[product_id[_]] = []
    product_by_id_dict[product_id[_]] = []
    if department[_] == "Men":
      product_gender_dict["M"] = []
      gender_category_dict["M" + category[_]] = []
    if department[_] == "Women":
      product_gender_dict["F"] = []
      gender_category_dict["F" + category[_]] = []
  for col in list(
      zip(
          product_id,
          brands,
          name,
          cost,
          category,
          department,
          sku,
          retail_price,
          distribution_center_id,
      )
  ):
    product_id = col[0]
    brand = col[1]
    name = col[2]
    cost = col[3]
    category = col[4]
    department = col[5]
    sku = col[6]
    retail_price = col[7]
    distribution_center_id = col[8]

    product_by_id_dict[product_id] = {
        "brand": brand,
        "name": name,
        "cost": cost,
        "category": category,
        "department": department,
        "sku": sku,
        "retail_price": retail_price,
        "distribution_center_id": distribution_center_id,
    }
    product_brand_dict[brand].append(col)
    product_category_dict[category].append(col)
    if department == "Men":
      product_gender_dict["M"].append(col)
      gender_category_dict["M" + category].append(col)
    if department == "Women":
      product_gender_dict["F"].append(col)
      gender_category_dict["F" + category].append(col)

  # helper dict to generate events
  for col in list(zip(product_id, brands, category, department)):
    product_id_dict[col[0]] = {
        "brand": col[1],
        "category": col[2],
        "department": col[3],
    }
  return product_gender_dict, product_by_id_dict, products


# read from local csv and return locations
def generate_locations() -> typing.List[str]:
  location_data = []
  with open(
      f"{os.environ['SOURCE_DIR']}/world_pop.csv", encoding="utf-8"
  ) as worldcsv:
    csvReader = csv.DictReader(worldcsv)
    for rows in csvReader:
      location_data.append(rows)
  return location_data


SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60
MINUTES_IN_DAY = 1440
MIN_AGE = 12
MAX_AGE = 71

products = generate_products()
logging.info("generating products helper dict")
logging.info("generating locations data")
LOCATION_DATA = generate_locations()
PRODUCT_GENDER_DICT = products[0]
PRODUCT_BY_ID_DICT = products[1]


def main(
    num_of_users: int,
    num_of_ghost_events: int,
    target_gcs_prefix: str,
    target_gcs_bucket: str,
    source_dir: str,
    extraneous_headers: typing.List[str],
) -> None:

  # read and generate location
  logging.info("generating data")
  for user_num in range(int(num_of_users)):
    logging.info(f"user transaction {user_num}")
    users.append(dataclasses.asdict(Users()))

  # remove extraneous keys in order_items
  logging.info("remove extraneous keys from order items")
  for oi in order_items:
    for key in extraneous_headers:
      del oi[key]

  # generate ghost events
  logging.info("generating ghost events")
  for user_num in range(int(num_of_users) * int(num_of_ghost_events)):
    logging.info(f"ghost event {user_num}")
    GhostEvents()

  # write generated data to gcs
  table_dat = [users, orders, order_items, events, inventory_items]
  table_name = ["users", "orders", "order_items", "events", "inventory_items"]
  for name, table_dat in list(zip(table_name, table_dat)):
    logging.info(f"converting {name} dict to csv")
    csv_data = dict_to_csv(table_dat)
    logging.info(
        "uploading output file to..."
        f" gs://{target_gcs_bucket}/{target_gcs_prefix}/{name}.csv"
    )
    upload_to_bucket(
        target_bucket=target_gcs_bucket,
        target_prefix=target_gcs_prefix,
        target_object=f"{name}.csv",
        source_data=csv_data,
    )

  # upload static data to gcs
  file_names = ["products.csv", "distribution_centers.csv"]
  for file in file_names:
    logging.info(
        "uploading output file to..."
        f" gs://{target_gcs_bucket}/{target_gcs_prefix}/{file}"
    )
    upload_to_bucket(
        target_bucket=target_gcs_bucket,
        target_prefix=target_gcs_prefix,
        target_object=f"{file}",
        source_filepath=f"{source_dir}/{file}",
    )


# returns random address based off specified distribution
def get_address(
    *, country: str = "*", state: str = "*", postal_code: str = "*"
) -> dict:
  # country = '*' OR country = 'USA' OR country={'USA':.75,'UK':.25}
  # state = '*' OR state = 'California' OR state={'California':.75,'New York':.25}
  # postal_code = '*' OR postal_code = '95060' OR postal_code={'94117':.75,'95060':.25}
  # type checking is used to provide flexibility of inputs to function (ie. can be dict with proportions, or could be single string value)
  universe = []
  if postal_code != "*":
    if isinstance(postal_code, str):
      universe += list(
          filter(lambda row: row["postal_code"] == postal_code, LOCATION_DATA)
      )
    elif isinstance(postal_code, dict):
      universe += list(
          filter(
              lambda row: row["postal_code"] in postal_code.keys(),
              LOCATION_DATA,
          )
      )
  if state != "*":
    if isinstance(state, str):
      universe += list(filter(lambda row: row["state"] == state, LOCATION_DATA))
    elif isinstance(state, dict):
      universe += list(
          filter(lambda row: row["state"] in state.keys(), LOCATION_DATA)
      )
  if country != "*":
    if isinstance(country, str) == str:
      universe += list(
          filter(lambda row: row["country"] == country, LOCATION_DATA)
      )
    elif isinstance(country, dict):
      universe += list(
          filter(lambda row: row["country"] in country.keys(), LOCATION_DATA)
      )
  if len(universe) == 0:
    universe = LOCATION_DATA

  total_pop = sum([int(loc["population"]) for loc in universe])

  for loc in universe:
    loc["population"] = int(loc["population"])
    if isinstance(postal_code, dict):
      if loc["postal_code"] in postal_code.keys():
        loc["population"] = postal_code[loc["postal_code"]] * total_pop
    if isinstance(state, dict):
      if loc["state"] in state.keys():
        loc["population"] = (
            state[loc["state"]]
            * (
                loc["population"]
                / sum([
                    loc2["population"]
                    for loc2 in universe
                    if loc["state"] == loc2["state"]
                ])
            )
            * total_pop
        )
    if isinstance(country, dict):
      if loc["country"] in country.keys():
        loc["population"] = (
            country[loc["country"]]
            * (
                loc["population"]
                / sum([
                    loc2["population"]
                    for loc2 in universe
                    if loc["country"] == loc2["country"]
                ])
            )
            * total_pop
        )

  loc = random.choices(
      universe, weights=[loc["population"] / total_pop for loc in universe]
  )[0]
  return {
      "street": fake.street_address(),
      "city": loc["city"],
      "state": loc["state"],
      "postal_code": loc["postal_code"],
      "country": loc["country"],
      "latitude": loc["latitude"],
      "longitude": loc["longitude"],
  }


# generates random date between now and specified date
def created_at(start_date: datetime.datetime) -> datetime.datetime:
  end_date = datetime.datetime.now()
  time_between_dates = end_date - start_date
  days_between_dates = time_between_dates.days
  if days_between_dates <= 1:
    days_between_dates = 2
  random_number_of_days = random.randrange(1, days_between_dates)
  created_at = (
      start_date
      + datetime.timedelta(days=random_number_of_days)
      + datetime.timedelta(minutes=random.randrange(MINUTES_IN_HOUR * 19))
  )
  return created_at


# generate URI for events table
def generate_uri(event: str, product: str) -> str:
  if event == "product":
    return f"/{event}/{product[0]}"
  elif event == "department":
    return f"""/{event}/{product[5].lower()}/category/{product[4].lower().replace(" ", "")}/brand/{product[1].lower().replace(" ", "")}"""
  else:
    return f"/{event}"


# converts list of dicts into csv format
def dict_to_csv(data: dict) -> str:
  output = io.StringIO()
  writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
  header_writer = csv.DictWriter(output, fieldnames=data[0].keys())
  header_writer.writeheader()
  for dat in data:
    writer.writerow(dat.values())
  return output.getvalue()


# upload into GCS Bucket
def upload_to_bucket(
    target_bucket: str,
    target_prefix: str,
    target_object: str,
    source_data: list = None,
    source_filepath: str = None,
) -> str:
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(target_bucket)
  blob = bucket.blob(f"{target_prefix}/{target_object}")

  if source_data:
    blob.upload_from_string(str(source_data), content_type="text/csv")
  else:
    blob.upload_from_filename(source_filepath)
  return blob.public_url


# utility class
class DataUtil:

  def child_created_at(self, probability: str = "uniform") -> datetime.datetime:
    # Calculate the total time elapsed since the parent was created
    time_between_dates = datetime.datetime.now() - self.parent.created_at

    # Calculate a random time delta within that duration
    random_time_seconds = random.randrange(
        int(time_between_dates.total_seconds())
    )

    # The new created_at is the parent's created_at plus the random time delta
    created_at = self.parent.created_at + datetime.timedelta(
        seconds=random_time_seconds
    )

    return created_at

  def random_item(
      self, population, **distribution
  ) -> str:  # returns single random item from a list based off distribution
    if distribution:
      return random.choices(
          population=population, weights=distribution["distribution"]
      )[0]
    else:
      return random.choices(population=population)[0]


@dataclasses.dataclass
class Address(object):

  def __init__(self, data: dict):
    self.street = data["street"]
    self.city = data["city"]
    self.state = data["state"]
    self.postal_code = data["postal_code"]
    self.country = data["country"]
    self.latitude = data["latitude"]
    self.longitude = data["longitude"]

  def __str__(self):
    return (
        f"{self.street} \n{self.city},"
        f" {self.state} \n{self.postal_code} \n{self.country} \n{self.latitude} \n{self.longitude}"
    )


@dataclasses.dataclass
class Users(DataUtil):
  logging.info("generating user")
  id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
  first_name: str = dataclasses.field(init=False)
  last_name: str = dataclasses.field(init=False)
  email: str = dataclasses.field(init=False)
  age: int = dataclasses.field(init=False)
  gender: str = dataclasses.field(init=False)
  state: str = dataclasses.field(init=False)
  street_address: str = dataclasses.field(init=False)
  postal_code: str = dataclasses.field(init=False)
  city: str = dataclasses.field(init=False)
  country: str = dataclasses.field(init=False)
  latitude: float = dataclasses.field(init=False)
  longitude: float = dataclasses.field(init=False)
  traffic_source: str = dataclasses.field(init=False)
  created_at: datetime.datetime = dataclasses.field(init=False)

  def __post_init__(self):
    self.gender = self.random_item(
        population=["M", "F"]
    )  # uniform distribution
    if self.gender == "M":
      self.first_name = fake.first_name_male()
      self.traffic_source = self.random_item(
          population=["Organic", "Facebook", "Search", "Email", "Display"],
          distribution=[0.15, 0.06, 0.7, 0.05, 0.04],
      )
    if self.gender == "F":
      self.first_name = fake.first_name_female()
      self.traffic_source = self.random_item(
          population=["Organic", "Facebook", "Search", "Email", "Display"],
          distribution=[0.15, 0.06, 0.7, 0.05, 0.04],
      )
    self.last_name = fake.last_name_nonbinary()
    address = Address(get_address())
    self.state = address.state
    self.street_address = address.street
    self.postal_code = address.postal_code
    self.city = address.city
    self.country = address.country
    self.latitude = address.latitude
    self.longitude = address.longitude
    self.email = f"{self.first_name.lower()}{self.last_name.lower()}@{fake.safe_domain_name()}"
    self.age = random.randrange(MIN_AGE, MAX_AGE)
    # weight newer users/orders
    choice = random.choices([0, 1], weights=[0.975, 0.025])[0]
    if choice == 0:
      self.created_at = created_at(datetime.datetime(2019, 1, 1))
    if choice == 1:
      self.created_at = created_at(
          datetime.datetime.now() - datetime.timedelta(days=7)
      )
    num_of_orders = random.choices(
        population=[0, 1, 2, 3, 4], weights=[0.2, 0.5, 0.2, 0.05, 0.05]
    )[0]
    if num_of_orders == 0:
      pass
    else:
      for _ in range(num_of_orders):
        orders.append(dataclasses.asdict(Order(user=self)))

  def __str__(self):
    return (
        f"{self.id}, {self.first_name}, {self.last_name}, {self.email},"
        f" {self.age}, {self.gender}, {self.state}, {self.street_address},"
        f" {self.postal_code}, {self.city}, {self.traffic_source},"
        f" {self.created_at}"
    )


@dataclasses.dataclass
class Product:
  logging.info("generating product")
  product_id: int = dataclasses.field(init=False)
  brand: str = dataclasses.field(init=False)
  name: str = dataclasses.field(init=False)
  cost: float = dataclasses.field(init=False)
  category: str = dataclasses.field(init=False)
  department: str = dataclasses.field(init=False)
  sku: str = dataclasses.field(init=False)
  retail_price: float = dataclasses.field(init=False)
  distribution_center_id: int = dataclasses.field(init=False)

  def __post_init__(self):
    person = Users()
    random_idx = np.random.choice(
        a=len(PRODUCT_GENDER_DICT[person.gender]), size=1
    )[0]
    product = PRODUCT_GENDER_DICT[person.gender][random_idx]
    self.brand = product[0]
    self.name = product[1]
    self.cost = product[2]
    self.category = product[3]
    self.department = product[4]
    self.sku = product[5]
    self.retail_price = product[6]
    self.distribution_center_id = product[7]

  def __str__(self):
    return (
        f"{self.brand}, {self.name}, {self.cost}, {self.category},"
        f" {self.department}, {self.sku}, {self.retail_price},"
        f" {self.distribution_center_id}"
    )


@dataclasses.dataclass
class Order(DataUtil):
  logging.info("generating order")
  order_id: int = dataclasses.field(
      default_factory=itertools.count(start=1).__next__
  )
  user_id: int = dataclasses.field(init=False)
  status: str = dataclasses.field(init=False)
  gender: str = dataclasses.field(init=False)
  created_at: datetime.datetime = dataclasses.field(init=False)
  returned_at: datetime.datetime = dataclasses.field(init=False)
  shipped_at: datetime.datetime = dataclasses.field(init=False)
  delivered_at: datetime.datetime = dataclasses.field(init=False)
  num_of_item: int = dataclasses.field(init=False)
  user: dataclasses.InitVar[typing.Any] = None

  def __post_init__(self, user=None):
    self.parent = user
    self.user_id = user.id
    self.gender = user.gender
    self.status = self.random_item(
        population=[
            "Complete",
            "Cancelled",
            "Returned",
            "Processing",
            "Shipped",
        ],
        distribution=[0.25, 0.15, 0.1, 0.2, 0.3],
    )
    self.created_at = self.child_created_at()
    # add random generator for days it takes to ship, deliver, return etc.
    if self.status == "Returned":
      self.shipped_at = self.created_at + datetime.timedelta(
          minutes=random.randrange(MINUTES_IN_DAY * 3)
      )  # shipped between 0-3 days after order placed
      self.delivered_at = self.shipped_at + datetime.timedelta(
          minutes=random.randrange(MINUTES_IN_DAY * 5)
      )  # delivered between 0-5 days after ship date
      self.returned_at = self.delivered_at + datetime.timedelta(
          minutes=random.randrange(MINUTES_IN_DAY * 3)
      )  # returned 0-3 days after order is delivered
    elif self.status == "Complete":
      self.shipped_at = self.created_at + datetime.timedelta(
          minutes=random.randrange(MINUTES_IN_DAY * 3)
      )  # shipped between 0-3 days after order placed
      self.delivered_at = self.shipped_at + datetime.timedelta(
          minutes=random.randrange(MINUTES_IN_DAY * 5)
      )  # delivered between 0-5 days after ship date
      self.returned_at = None
    elif self.status == "Shipped":
      self.shipped_at = self.created_at + datetime.timedelta(
          minutes=random.randrange(MINUTES_IN_DAY * 3)
      )  # shipped between 0-3 days after order placed
      self.delivered_at = None
      self.returned_at = None
    else:
      self.shipped_at = None
      self.delivered_at = None
      self.returned_at = None
    self.user = user  # pass person object to order_items
    # randomly generate number of items in an order
    num_of_items = self.random_item(
        population=[1, 2, 3, 4], distribution=[0.7, 0.2, 0.05, 0.05]
    )
    self.num_of_item = num_of_items
    for _ in range(num_of_items):
      order_items.append(dataclasses.asdict(OrderItem(order=self)))

  def __str__(self):
    return (
        f"{self.order_id}, {self.user_id}, {self.status}, {self.created_at},"
        f" {self.shipped_at}, {self.delivered_at}, {self.returned_at}"
    )


@dataclasses.dataclass
class Events:
  logging.info("generating event")
  id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
  user_id: int = dataclasses.field(init=False)
  sequence_number: int = dataclasses.field(init=False)
  session_id: str = dataclasses.field(init=False)
  created_at: datetime.datetime = dataclasses.field(init=False)
  # inventory_item_id:int = field(init=False)
  ip_address: str = dataclasses.field(init=False)
  city: str = dataclasses.field(init=False)
  state: str = dataclasses.field(init=False)
  postal_code: str = dataclasses.field(init=False)
  browser: str = dataclasses.field(init=False)
  traffic_source: str = dataclasses.field(init=False)
  uri: str = dataclasses.field(init=False)
  event_type: str = dataclasses.field(init=False)
  order_item: dataclasses.InitVar[typing.Any] = None

  def __post_init__(self, order_item=None):
    self.sequence_number = order_item.sequence_number
    self.user_id = order_item.user_id
    self.created_at = order_item.created_at
    self.session_id = order_item.session_id
    self.ip_address = order_item.ip_address
    self.city = order_item.person.city
    self.state = order_item.person.state
    self.postal_code = order_item.person.postal_code
    self.event_type = order_item.event_type
    self.browser = order_item.browser
    self.uri = order_item.uri
    self.traffic_source = order_item.traffic_source

  def __str__(self):
    return (
        f"{self.created_at}, {self.ip_address}, {self.city}, {self.state},"
        f" {self.postal_code}"
    )


inv_item_id = 0


@dataclasses.dataclass
class OrderItem(DataUtil):
  logging.info("generating order item")
  id: int = dataclasses.field(default_factory=itertools.count(start=1).__next__)
  order_id: int = dataclasses.field(init=False)
  user_id: int = dataclasses.field(init=False)
  product_id: int = dataclasses.field(init=False)
  inventory_item_id: int = dataclasses.field(init=False)
  status: str = dataclasses.field(init=False)
  created_at: datetime.datetime = dataclasses.field(init=False)
  shipped_at: datetime.datetime = dataclasses.field(init=False)
  delivered_at: datetime.datetime = dataclasses.field(init=False)
  returned_at: datetime.datetime = dataclasses.field(init=False)

  sale_price: float = dataclasses.field(init=False)

  # extras
  event_type: str = dataclasses.field(init=False)
  ip_address: str = dataclasses.field(init=False)
  browser: str = dataclasses.field(init=False)
  traffic_source: str = dataclasses.field(init=False)
  session_id: str = dataclasses.field(init=False)
  sequence_number: int = dataclasses.field(init=False)
  uri: str = dataclasses.field(init=False)
  is_sold: bool = dataclasses.field(init=False)
  order: dataclasses.InitVar[typing.Any] = None

  def __post_init__(self, order=None):
    global inv_item_id

    self.order_id = order.order_id
    self.user_id = order.user_id
    inv_item_id = inv_item_id + 1
    self.inventory_item_id = inv_item_id
    self.status = order.status
    self.created_at = order.created_at - datetime.timedelta(
        seconds=random.randrange(SECONDS_IN_MINUTE * 240)
    )  # order purchased within 4 hours

    self.shipped_at = order.shipped_at
    self.delivered_at = order.delivered_at
    self.returned_at = order.returned_at

    random_idx = np.random.choice(
        a=len(PRODUCT_GENDER_DICT[order.gender]), size=1
    )[0]
    product = PRODUCT_GENDER_DICT[order.gender][random_idx]
    self.product_id = product[0]
    self.sale_price = product[7]
    self.ip_address = fake.ipv4()
    self.browser = self.random_item(
        population=["IE", "Chrome", "Safari", "Firefox", "Other"],
        distribution=[0.05, 0.5, 0.2, 0.2, 0.05],
    )
    self.traffic_source = self.random_item(
        population=["Email", "Adwords", "Organic", "YouTube", "Facebook"],
        distribution=[0.45, 0.3, 0.05, 0.1, 0.1],
    )
    self.session_id = str(uuid.uuid4())

    self.person = order.user  # pass person object to events
    self.is_sold = True
    previous_created_at = None

    # Generate Events Table
    if order.num_of_item == 1:  # if only 1 item in order go through flow
      for idx, val in enumerate(
          ["home", "department", "product", "cart", "purchase"]
      ):
        self.sequence_number = idx + 1
        self.event_type = val
        self.uri = generate_uri(val, product)
        events.append(dataclasses.asdict(Events(order_item=self)))
        previous_created_at = self.created_at
        self.created_at = previous_created_at + datetime.timedelta(
            seconds=random.randrange(SECONDS_IN_MINUTE * 3)
        )
    else:  # if multiple items
      sequence_num = 0  # track sequence num of purchase event
      for _ in range(order.num_of_item):
        for event in ["department", "product", "cart"]:
          sequence_num += 1
          self.sequence_number = sequence_num
          self.event_type = event
          self.uri = generate_uri(event, product)
          events.append(dataclasses.asdict(Events(order_item=self)))
          sequence_num = self.sequence_number
          previous_created_at = self.created_at
          self.created_at = previous_created_at + datetime.timedelta(
              seconds=random.randrange(180)
          )
      self.sequence_number = sequence_num + 1
      self.created_at += datetime.timedelta(random.randrange(5))
      self.event_type = "purchase"
      self.uri = generate_uri("purchase", product)
      events.append(dataclasses.asdict(Events(order_item=self)))

    # sold inventory item
    inventory_items.append(dataclasses.asdict(InventoryItem(order_item=self)))

    # unsold inventory items
    num_of_items = self.random_item(
        population=[1, 2, 3], distribution=[0.5, 0.3, 0.2]
    )
    for _ in range(num_of_items):
      self.is_sold = False
      inv_item_id += 1
      self.inventory_item_id = inv_item_id
      inventory_items.append(dataclasses.asdict(InventoryItem(order_item=self)))


@dataclasses.dataclass
class InventoryItem:
  id: int = dataclasses.field(init=False)
  product_id: int = dataclasses.field(init=False)
  created_at: datetime.datetime = dataclasses.field(init=False)
  sold_at: datetime.datetime = dataclasses.field(init=False)
  cost: float = dataclasses.field(init=False)
  product_category: str = dataclasses.field(init=False)
  product_name: str = dataclasses.field(init=False)
  product_brand: str = dataclasses.field(init=False)
  product_retail_price: float = dataclasses.field(init=False)
  product_department: str = dataclasses.field(init=False)
  product_sku: str = dataclasses.field(init=False)
  product_distribution_center_id: int = dataclasses.field(init=False)
  order_item: dataclasses.InitVar[typing.Any] = None

  def __post_init__(self, order_item=None):
    self.id = order_item.inventory_item_id
    self.product_id = order_item.product_id
    if order_item.is_sold is True:
      self.created_at = order_item.created_at - datetime.timedelta(
          minutes=random.randrange(86400)
      )  # in inventory between 0 and 60 days
      self.sold_at = (
          order_item.created_at
      )  # sold on the date/time the order_items was logged
    if order_item.is_sold is False:
      self.created_at = created_at(datetime.datetime(2020, 1, 1))
      self.sold_at = None
    self.cost = PRODUCT_BY_ID_DICT[self.product_id]["cost"]
    self.product_category = PRODUCT_BY_ID_DICT[self.product_id]["category"]
    self.product_name = PRODUCT_BY_ID_DICT[self.product_id]["name"]
    self.product_brand = PRODUCT_BY_ID_DICT[self.product_id]["brand"]
    self.product_retail_price = PRODUCT_BY_ID_DICT[self.product_id][
        "retail_price"
    ]
    self.product_department = PRODUCT_BY_ID_DICT[self.product_id]["department"]
    self.product_sku = PRODUCT_BY_ID_DICT[self.product_id]["sku"]
    self.product_distribution_center_id = PRODUCT_BY_ID_DICT[self.product_id][
        "distribution_center_id"
    ]

  def __str__(self):
    return (
        f"{self.id}, {self.product_id}, {self.created_at}, {self.cost},"
        f" {self.product_category}, {self.product_name}, {self.product_brand},"
        f" {self.product_retail_price}, {self.product_department},"
        f" {self.product_sku}, {self.product_distribution_center_id}"
    )


@dataclasses.dataclass
class GhostEvents(DataUtil):
  id: int = dataclasses.field(init=False)
  user_id: int = dataclasses.field(init=False)
  sequence_number: int = dataclasses.field(init=False)
  session_id: str = dataclasses.field(init=False)
  created_at: datetime.datetime = dataclasses.field(init=False)
  ip_address: str = dataclasses.field(init=False)
  city: str = dataclasses.field(init=False)
  state: str = dataclasses.field(init=False)
  postal_code: str = dataclasses.field(init=False)
  browser: str = dataclasses.field(init=False)
  traffic_source: str = dataclasses.field(init=False)
  uri: str = dataclasses.field(init=False)
  event_type: str = dataclasses.field(init=False)

  def __post_init__(self):
    address = get_address()
    self.sequence_number = 0
    self.user_id = None
    self.created_at = created_at(datetime.datetime(2019, 1, 1))
    self.session_id = str(uuid.uuid4())
    self.ip_address = fake.ipv4()
    self.city = address["city"]
    self.state = address["state"]
    self.postal_code = address["postal_code"]
    self.browser = self.random_item(
        population=["IE", "Chrome", "Safari", "Firefox", "Other"],
        distribution=[0.05, 0.5, 0.2, 0.2, 0.05],
    )
    self.traffic_source = self.random_item(
        population=["Email", "Adwords", "Organic", "YouTube", "Facebook"],
        distribution=[0.45, 0.3, 0.05, 0.1, 0.1],
    )

    products = PRODUCT_GENDER_DICT[
        self.random_item(population=["M", "F"], distribution=[0.5, 0.5])
    ]
    product = self.random_item(products)

    # different event type combinations
    cancelled_browsing = ["product", "cart", "cancel"]
    abandoned_cart = ["department", "product", "cart"]
    viewed_product = ["product"]
    viewed_department = ["department", "product"]

    random_events = self.random_item(
        population=[
            cancelled_browsing,
            abandoned_cart,
            viewed_product,
            viewed_department,
        ]
    )

    for event in random_events:
      # set ghost events ID to max of original
      event_id = len(events)
      self.id = event_id + 1
      event_id = self.id

      self.event_type = event
      self.uri = generate_uri(event, product)
      self.sequence_number += 1
      self.created_at = self.created_at + datetime.timedelta(
          minutes=random.randrange(int(MINUTES_IN_HOUR * 0.5))
      )
      events.append(dataclasses.asdict(self))

  def __str__(self):
    return (
        f"{self.created_at}, {self.ip_address}, {self.city}, {self.state},"
        f" {self.postal_code}"
    )


if __name__ == "__main__":
  logging.getLogger().setLevel(logging.INFO)
  main(
      num_of_users=int(os.environ["NUM_OF_USERS"]),
      num_of_ghost_events=int(os.environ["NUM_OF_GHOST_EVENTS"]),
      target_gcs_prefix=os.environ["TARGET_GCS_PREFIX"],
      target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
      source_dir=os.environ["SOURCE_DIR"],
      extraneous_headers=json.loads(os.environ["EXTRANEOUS_HEADERS"]),
  )
