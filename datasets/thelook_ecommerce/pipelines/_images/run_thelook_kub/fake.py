import csv
import itertools
import json
import logging
import os
import random
import typing
import uuid
from collections import defaultdict
from dataclasses import InitVar, asdict, dataclass, field
from datetime import datetime, timedelta
from io import StringIO
from random import randrange
from typing import Any
import numpy as np
from faker import Faker
from google.cloud import storage

fake = Faker()
# final datasets
orders = list()
users = list()
order_items = list()
events = list()
inventory_items = list()


def main(
    num_of_users: int, target_gcs_bucket: str, extraneous_headers: typing.List[str]
):
    global product_gender_dict
    global product_by_id_dict
    global location_data

    logging.info("generating products helper dict")
    products = generate_products()

    product_gender_dict = products[0]
    product_by_id_dict = products[1]

    logging.info("generating locations data")
    location_data = generate_locations()

    # read and generate location
    logging.info("generating data")
    for i in range(int(num_of_users)):
        logging.info(f"user transaction {i}")
        users.append(asdict(Users()))

    # remove extraneous keys in order_items
    logging.info("remove extraneous keys from order items")
    # order_item_remove_keys = ["event_type", "ip_address", "browser", "traffic_source", "session_id", "sequence_number", "uri", "is_sold"]
    for oi in order_items:
        for key in extraneous_headers:
            del oi[key]

    # generate ghost events
    logging.info("generating ghost events")
    for i in range(int(num_of_users)):
        logging.info(f"ghost event {i}")
        Ghost_Events()

    # write generated data to gcs
    table_dat = [users, orders, order_items, events, inventory_items]
    table_name = ["users", "orders", "order_items", "events", "inventory_items"]
    for name, table_dat in list(zip(table_name, table_dat)):
        logging.info(f"converting {name} dict to csv")
        csv_data = dict_to_csv(name, table_dat)
        logging.info(
            f"uploading output file to... gs://{target_gcs_bucket}/data/{name}.csv"
        )
        upload_to_bucket(
            bucket_name=target_gcs_bucket, file_name=name, data=str(csv_data)
        )

    # upload static data to gcs
    file_name = ["products.csv", "distribution_centers.csv"]
    for i in file_name:
        logging.info(f"uploading output file to... gs://{target_gcs_bucket}/data/{i}")
        upload_file_to_bucket(bucket_name=target_gcs_bucket, file_name=i)


# read from local csv and return products
def generate_products():
    product_brand_dict = {}  # products partitioned by brand - unused
    product_category_dict = {}  # product partitioned by cateogry - unused
    gender_category_dict = {}  # products partitioned by gender and category - unused
    product_id_dict = {}  # products to generate events table - unused
    product_gender_dict = {}  # product partitioned by gender
    product_by_id_dict = {}  # products partitioned by product ID

    products = defaultdict(list)
    with open("data/products.csv", encoding="utf-8") as productcsv:
        csvReader = csv.DictReader(productcsv)
        for rows in csvReader:
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
    for val in list(
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
        product_by_id_dict[val[0]] = {
            "brand": val[1],
            "name": val[2],
            "cost": val[3],
            "category": val[4],
            "department": val[5],
            "sku": val[6],
            "retail_price": val[7],
            "distribution_center_id": val[8],
        }
        product_brand_dict[val[1]].append(val)
        product_category_dict[val[4]].append(val)
        if val[5] == "Men":
            product_gender_dict["M"].append(val)
            gender_category_dict["M" + val[4]].append(val)
        if val[5] == "Women":
            product_gender_dict["F"].append(val)
            gender_category_dict["F" + val[4]].append(val)

    # helper dict to generate events
    for val in list(zip(product_id, brands, category, department)):
        product_id_dict[val[0]] = {
            "brand": val[1],
            "category": val[2],
            "department": val[3],
        }
    return product_gender_dict, product_by_id_dict, products


# read from local csv and return locations
def generate_locations():
    location_data = []
    with open("data/world_pop.csv", encoding="utf-8") as worldcsv:
        csvReader = csv.DictReader(worldcsv)
        for rows in csvReader:
            location_data.append(rows)
    return location_data


# read from local csv and return distribution centers
def generate_distribution_centers():
    distribution_centers = []
    with open(
        "data/distribution_centers.csv", encoding="utf-8"
    ) as distributioncenterscsv:
        csvReader = csv.DictReader(distributioncenterscsv)
        for rows in csvReader:
            distribution_centers.append(rows)
    return distribution_centers


# returns random address based off specified distribution
def get_address(*, country="*", state="*", postal_code="*"):
    # country = '*' OR country = 'USA' OR country={'USA':.75,'UK':.25}
    # state = '*' OR state = 'California' OR state={'California':.75,'New York':.25}
    # postal_code = '*' OR postal_code = '95060' OR postal_code={'94117':.75,'95060':.25}
    universe = []
    if postal_code != "*":
        if type(postal_code) == str:
            universe += list(
                filter(lambda row: row["postal_code"] == postal_code, location_data)
            )
        elif type(postal_code) == dict:
            universe += list(
                filter(
                    lambda row: row["postal_code"] in postal_code.keys(), location_data
                )
            )
    if state != "*":
        if type(state) == str:
            universe += list(filter(lambda row: row["state"] == state, location_data))
        elif type(state) == dict:
            universe += list(
                filter(lambda row: row["state"] in state.keys(), location_data)
            )
    if country != "*":
        if type(country) == str:
            universe += list(
                filter(lambda row: row["country"] == country, location_data)
            )
        elif type(country) == dict:
            universe += list(
                filter(lambda row: row["country"] in country.keys(), location_data)
            )
    if len(universe) == 0:
        universe = location_data

    total_pop = sum([int(loc["population"]) for loc in universe])

    for loc in universe:
        loc["population"] = int(loc["population"])
        if type(postal_code) == dict:
            if loc["postal_code"] in postal_code.keys():
                loc["population"] = postal_code[loc["postal_code"]] * total_pop
        if type(state) == dict:
            if loc["state"] in state.keys():
                loc["population"] = (
                    state[loc["state"]]
                    * (
                        loc["population"]
                        / sum(
                            [
                                loc2["population"]
                                for loc2 in universe
                                if loc["state"] == loc2["state"]
                            ]
                        )
                    )
                    * total_pop
                )
        if type(country) == dict:
            if loc["country"] in country.keys():
                loc["population"] = (
                    country[loc["country"]]
                    * (
                        loc["population"]
                        / sum(
                            [
                                loc2["population"]
                                for loc2 in universe
                                if loc["country"] == loc2["country"]
                            ]
                        )
                    )
                    * total_pop
                )

    loc = random.choices(
        universe, weights=[loc["population"] / total_pop for loc in universe]
    )[0]
    return {
        "street": fake.street_address(),
        "city": loc["city"],
        "state": loc["country"],
        "postal_code": loc["postal_code"],
        "country": loc["country"],
        "latitude": loc["latitude"],
        "longitude": loc["longitude"],
    }


# generates random date between now and specified date
def created_at(start_date):
    end_date = datetime.now()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    if days_between_dates <= 1:
        days_between_dates = 2
    random_number_of_days = random.randrange(1, days_between_dates)
    created_at = (
        start_date
        + timedelta(days=random_number_of_days)
        + timedelta(minutes=randrange(1139))
    )
    return created_at


# generate URI for events table
def generate_uri(event, product):
    if event == "product":
        return "/" + event + "/" + product[0]
    elif event == "department":
        return (
            "/"
            + event
            + "/"
            + product[5].lower()
            + "/category/"
            + product[4].lower().replace(" ", "")
            + "/brand/"
            + product[1].lower().replace(" ", "")
        )
    else:
        return "/" + event


# converts list of dicts into csv format
def dict_to_csv(name, data):
    output = StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    header_writer = csv.DictWriter(output, fieldnames=data[0].keys())
    header_writer.writeheader()
    for dat in data:
        writer.writerow(dat.values())
    return output.getvalue()


# upload into GCS Bucket
def upload_to_bucket(bucket_name, file_name, data):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob("data/{}.csv".format(file_name))
    blob.upload_from_string(data, content_type="text/csv")
    return blob.public_url


# upload local file to GCS Bucket
def upload_file_to_bucket(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob("data/{}".format(file_name))
    blob.upload_from_filename("data/{}".format(file_name))
    return blob.public_url


# utility class
class DataUtil:
    def child_created_at(
        self, probability="uniform"
    ):  # returns a random timestamp between now and parent date
        time_between_dates = datetime.now() - self.parent.created_at
        days_between_dates = time_between_dates.days
        if days_between_dates <= 1:
            days_between_dates = 2
        random_number_of_days = random.randrange(
            1, days_between_dates
        )  # generates random day between now and when user initially got created
        created_at = self.parent.created_at + timedelta(days=random_number_of_days)
        return created_at

    def random_item(
        self, population, **distribution
    ):  # returns single random item from a list based off distribution
        if distribution:
            return random.choices(
                population=population, weights=distribution["distribution"]
            )[0]
        else:
            return random.choices(population=population)[0]


@dataclass
class Address(object):
    def __init__(self, data):
        self.street = data["street"]
        self.city = data["city"]
        self.state = data["state"]
        self.postal_code = data["postal_code"]
        self.country = data["country"]
        self.latitude = data["latitude"]
        self.longitude = data["longitude"]

    def __str__(self):
        return f"{self.street} \n{self.city}, {self.state} \n{self.postal_code} \n{self.country} \n{self.latitude} \n{self.longitude}"


@dataclass
class Users(DataUtil):
    logging.info("generating user")
    id: int = field(default_factory=itertools.count(start=1).__next__)
    first_name: str = field(init=False)
    last_name: str = field(init=False)
    email: str = field(init=False)
    gender: str = field(init=False)
    state: str = field(init=False)
    street_address: str = field(init=False)
    postal_code: str = field(init=False)
    city: str = field(init=False)
    country: str = field(init=False)
    latitude: float = field(init=False)
    longitude: float = field(init=False)
    traffic_source: str = field(init=False)
    created_at: datetime = field(init=False)

    def __post_init__(self):
        self.gender = self.random_item(population=["M", "F"])  # uniform distribution
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
        self.email = (
            self.first_name.lower()
            + self.last_name.lower()
            + "@"
            + fake.free_email_domain()
        )
        # weight newer users/orders
        choice = random.choices([0, 1], weights=[0.975, 0.025])[0]
        if choice == 0:
            self.created_at = created_at(datetime(2019, 1, 1))
        if choice == 1:
            self.created_at = created_at(datetime.now() - timedelta(days=7))
        num_of_orders = random.choices(
            population=[0, 1, 2, 3, 4], weights=[0.2, 0.5, 0.2, 0.05, 0.05]
        )[0]
        if num_of_orders == 0:
            pass
        else:
            for i in range(num_of_orders):
                orders.append(asdict(Order(user=self)))

    def __str__(self):
        return f"{self.id}, {self.first_name}, {self.last_name}, {self.email}, {self.gender}, {self.state}, {self.street_address}, {self.postal_code}, {self.city}, {self.traffic_source}, {self.created_at}"


@dataclass
class Product:
    logging.info("generating product")
    product_id: int = field(init=False)
    brand: str = field(init=False)
    name: str = field(init=False)
    cost: float = field(init=False)
    category: str = field(init=False)
    department: str = field(init=False)
    sku: str = field(init=False)
    retail_price: float = field(init=False)
    distribution_center_id: int = field(init=False)

    def __post_init__(self):
        person = Users()
        random_idx = np.random.choice(
            a=len(product_gender_dict[person.gender]), size=1
        )[0]
        product = product_gender_dict[person.gender][random_idx]
        self.brand = product[0]
        self.name = product[1]
        self.cost = product[2]
        self.category = product[3]
        self.department = product[4]
        self.sku = product[5]
        self.retail_price = product[6]
        self.distribution_center_id = product[7]

    def __str__(self):
        return f"{self.brand}, {self.name}, {self.cost}, {self.category}, {self.department}, {self.sku}, {self.retail_price}, {self.distribution_center_id}"


@dataclass
class Order(DataUtil):
    logging.info("generating order")
    order_id: int = field(default_factory=itertools.count(start=1).__next__)
    user_id: int = field(init=False)
    status: str = field(init=False)
    gender: str = field(init=False)
    created_at: datetime = field(init=False)
    returned_at: datetime = field(init=False)
    shipped_at: datetime = field(init=False)
    delivered_at: datetime = field(init=False)
    num_of_item: int = field(init=False)
    user: InitVar[Any] = None

    def __post_init__(self, user=None):
        self.parent = user
        self.user_id = user.id
        self.gender = user.gender
        self.status = self.random_item(
            population=["Complete", "Cancelled", "Returned"],
            distribution=[0.85, 0.05, 0.1],
        )
        self.created_at = self.child_created_at()
        # add random generator for days it takes to ship, deliver, return etc.
        if self.status == "Returned":
            self.shipped_at = self.created_at + timedelta(
                minutes=randrange(4320)
            )  # shipped between 0-3 days after order placed
            self.delivered_at = self.shipped_at + timedelta(
                minutes=randrange(7200)
            )  # delivered between 0-5 days after ship date
            self.returned_at = self.delivered_at + timedelta(
                minutes=randrange(4320)
            )  # returned 0-3 days after order is delivered
        elif self.status == "Complete":
            self.shipped_at = self.created_at + timedelta(
                minutes=randrange(4320)
            )  # shipped between 0-3 days after order placed
            self.delivered_at = self.shipped_at + timedelta(
                minutes=randrange(7200)
            )  # delivered between 0-5 days after ship date
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
        for i in range(num_of_items):
            order_items.append(asdict(Order_Item(order=self)))

    def __str__(self):
        return f"{self.order_id}, {self.user_id}, {self.status}, {self.created_at}, {self.shipped_at}, {self.delivered_at}, {self.returned_at}"


@dataclass
class Events:
    logging.info("generating event")
    id: int = field(default_factory=itertools.count(start=1).__next__)
    user_id: int = field(init=False)
    sequence_number: int = field(init=False)
    session_id: str = field(init=False)
    created_at: datetime = field(init=False)
    # inventory_item_id:int = field(init=False)
    ip_address: str = field(init=False)
    city: str = field(init=False)
    state: str = field(init=False)
    postal_code: str = field(init=False)
    # country:str = field(init=False)
    browser: str = field(init=False)
    traffic_source: str = field(init=False)
    uri: str = field(init=False)
    event_type: str = field(init=False)
    order_item: InitVar[Any] = None

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
        return f"{self.created_at}, {self.product_id}, {self.ip_address}, {self.city}, {self.state}, {self.postal_code}"


inv_item_id = 0


@dataclass
class Order_Item(DataUtil):
    logging.info("generating order item")
    id: int = field(default_factory=itertools.count(start=1).__next__)
    order_id: int = field(init=False)
    user_id: int = field(init=False)
    product_id: int = field(init=False)
    inventory_item_id: int = field(init=False)
    created_at: datetime = field(init=False)

    shipped_at: datetime = field(init=False)
    delivered_at: datetime = field(init=False)
    returned_at: datetime = field(init=False)

    sale_price: float = field(init=False)

    # extras
    event_type: str = field(init=False)
    ip_address: str = field(init=False)
    browser: str = field(init=False)
    traffic_source: str = field(init=False)
    session_id: str = field(init=False)
    sequence_number: int = field(init=False)
    uri: str = field(init=False)
    is_sold: bool = field(init=False)
    order: InitVar[Any] = None

    def __post_init__(self, order=None):
        global inv_item_id

        self.order_id = order.order_id
        self.user_id = order.user_id
        inv_item_id = inv_item_id + 1
        self.inventory_item_id = inv_item_id
        # self.created_at = datetime.combine(order.created_at, datetime.min.time()) - timedelta(seconds=randrange(60)) #order purchased within 4 hours
        self.created_at = order.created_at - timedelta(
            seconds=randrange(14400)
        )  # order purchased within 4 hours

        self.shipped_at = order.shipped_at
        self.delivered_at = order.delivered_at
        self.returned_at = order.returned_at

        random_idx = np.random.choice(a=len(product_gender_dict[order.gender]), size=1)[
            0
        ]
        product = product_gender_dict[order.gender][random_idx]
        self.product_id = product[0]
        self.sale_price = product[3]
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
                events.append(asdict(Events(order_item=self)))
                previous_created_at = self.created_at
                self.created_at = previous_created_at + timedelta(
                    seconds=randrange(180)
                )
        else:  # if multiple items
            sequence_num = 0  # track sequence num of purchase event
            for i in range(order.num_of_item):
                for j in ["department", "product", "cart"]:
                    sequence_num += 1
                    self.sequence_number = sequence_num
                    self.event_type = j
                    self.uri = generate_uri(j, product)
                    events.append(asdict(Events(order_item=self)))
                    sequence_num = self.sequence_number
                    previous_created_at = self.created_at
                    self.created_at = previous_created_at + timedelta(
                        seconds=randrange(180)
                    )
            self.sequence_number = sequence_num + 1
            self.created_at += timedelta(randrange(5))
            self.event_type = "purchase"
            self.uri = generate_uri("purchase", product)
            events.append(asdict(Events(order_item=self)))

        # sold inventory item
        inventory_items.append(asdict(Inventory_Item(order_item=self)))

        # unsold inventory items
        num_of_items = self.random_item(
            population=[1, 2, 3], distribution=[0.5, 0.3, 0.2]
        )
        for i in range(num_of_items):
            self.is_sold = False
            inv_item_id += 1
            self.inventory_item_id = inv_item_id
            inventory_items.append(asdict(Inventory_Item(order_item=self)))


@dataclass
class Inventory_Item:
    id: int = field(init=False)
    product_id: int = field(init=False)
    created_at: datetime = field(init=False)
    sold_at: datetime = field(init=False)
    cost: float = field(init=False)
    product_category: str = field(init=False)
    product_name: str = field(init=False)
    product_brand: str = field(init=False)
    product_retail_price: float = field(init=False)
    product_department: str = field(init=False)
    product_sku: str = field(init=False)
    product_distribution_center_id: int = field(init=False)
    order_item: InitVar[Any] = None

    def __post_init__(self, order_item=None):
        self.id = order_item.inventory_item_id
        self.product_id = order_item.product_id
        if order_item.is_sold is True:
            self.created_at = order_item.created_at - timedelta(
                minutes=randrange(86400)
            )  # in inventory between 0 and 60 days
            self.sold_at = (
                order_item.created_at
            )  # sold on the date/time the order_items was logged
        if order_item.is_sold is False:
            self.created_at = created_at(datetime(2020, 1, 1))
            self.sold_at = None
        self.cost = product_by_id_dict[self.product_id]["cost"]
        self.product_category = product_by_id_dict[self.product_id]["category"]
        self.product_name = product_by_id_dict[self.product_id]["name"]
        self.product_brand = product_by_id_dict[self.product_id]["brand"]
        self.product_retail_price = product_by_id_dict[self.product_id]["retail_price"]
        self.product_department = product_by_id_dict[self.product_id]["department"]
        self.product_sku = product_by_id_dict[self.product_id]["sku"]
        self.product_distribution_center_id = product_by_id_dict[self.product_id][
            "distribution_center_id"
        ]

    def __str__(self):
        return f"{self.id}, {self.product_id}, {self.created_at}, {self.cost}, {self.product_category}, {self.product_name}, {self.product_brand}, {self.product_retail_price}, {self.product_department}, {self.product_sku}, {self.product_distribution_center_id}"


@dataclass
class Ghost_Events(DataUtil):
    id: int = field(init=False)
    user_id: int = field(init=False)
    sequence_number: int = field(init=False)
    session_id: str = field(init=False)
    created_at: datetime = field(init=False)
    ip_address: str = field(init=False)
    city: str = field(init=False)
    state: str = field(init=False)
    postal_code: str = field(init=False)
    browser: str = field(init=False)
    traffic_source: str = field(init=False)
    uri: str = field(init=False)
    event_type: str = field(init=False)

    def __post_init__(self):
        address = get_address()
        self.sequence_number = 0
        self.user_id = None
        self.created_at = created_at(datetime(2019, 1, 1))
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

        products = product_gender_dict[
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

        for i in random_events:
            # set ghost events ID to max of original
            event_id = len(events)
            self.id = event_id + 1
            event_id = self.id

            self.event_type = i
            self.uri = generate_uri(i, product)
            self.sequence_number += 1
            self.created_at = self.created_at + timedelta(minutes=randrange(30))
            events.append(asdict(self))

    def __str__(self):
        return f"{self.created_at}, {self.product_id}, {self.ip_address}, {self.city}, {self.state}, {self.postal_code}"


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        num_of_users=os.environ["NUM_OF_USERS"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        extraneous_headers=json.loads(os.environ["EXTRANEOUS_HEADERS"]),
    )

    # main(target_gcs_bucket="us-central1-thelook-faker-d1ecf43a-bucket")

# ["event_type", "ip_address", "browser", "traffic_source", "session_id", "sequence_number", "uri", "is_sold"]
