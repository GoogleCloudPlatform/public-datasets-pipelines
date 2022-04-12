/**
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


resource "google_bigquery_table" "thelook_ecommerce_products" {
  project     = var.project_id
  dataset_id  = "thelook_ecommerce"
  table_id    = "products"
  description = "The Look fictitious e-commerce dataset - products table"
  depends_on = [
    google_bigquery_dataset.thelook_ecommerce
  ]
}

output "bigquery_table-thelook_ecommerce_products-table_id" {
  value = google_bigquery_table.thelook_ecommerce_products.table_id
}

output "bigquery_table-thelook_ecommerce_products-id" {
  value = google_bigquery_table.thelook_ecommerce_products.id
}

resource "google_bigquery_table" "thelook_ecommerce_events" {
  project     = var.project_id
  dataset_id  = "thelook_ecommerce"
  table_id    = "events"
  description = "Programatically generated web events for The Look fictitious e-commerce store"
  depends_on = [
    google_bigquery_dataset.thelook_ecommerce
  ]
}

output "bigquery_table-thelook_ecommerce_events-table_id" {
  value = google_bigquery_table.thelook_ecommerce_events.table_id
}

output "bigquery_table-thelook_ecommerce_events-id" {
  value = google_bigquery_table.thelook_ecommerce_events.id
}

resource "google_bigquery_table" "thelook_ecommerce_users" {
  project     = var.project_id
  dataset_id  = "thelook_ecommerce"
  table_id    = "users"
  description = "Programatically generated users for The Look fictitious e-commerce store"
  depends_on = [
    google_bigquery_dataset.thelook_ecommerce
  ]
}

output "bigquery_table-thelook_ecommerce_users-table_id" {
  value = google_bigquery_table.thelook_ecommerce_users.table_id
}

output "bigquery_table-thelook_ecommerce_users-id" {
  value = google_bigquery_table.thelook_ecommerce_users.id
}

resource "google_bigquery_table" "thelook_ecommerce_orders" {
  project     = var.project_id
  dataset_id  = "thelook_ecommerce"
  table_id    = "orders"
  description = "Programatically generated orders for The Look fictitious e-commerce store"
  depends_on = [
    google_bigquery_dataset.thelook_ecommerce
  ]
}

output "bigquery_table-thelook_ecommerce_orders-table_id" {
  value = google_bigquery_table.thelook_ecommerce_orders.table_id
}

output "bigquery_table-thelook_ecommerce_orders-id" {
  value = google_bigquery_table.thelook_ecommerce_orders.id
}

resource "google_bigquery_table" "thelook_ecommerce_order_items" {
  project     = var.project_id
  dataset_id  = "thelook_ecommerce"
  table_id    = "order_items"
  description = "Programatically generated order items for The Look fictitious e-commerce store"
  depends_on = [
    google_bigquery_dataset.thelook_ecommerce
  ]
}

output "bigquery_table-thelook_ecommerce_order_items-table_id" {
  value = google_bigquery_table.thelook_ecommerce_order_items.table_id
}

output "bigquery_table-thelook_ecommerce_order_items-id" {
  value = google_bigquery_table.thelook_ecommerce_order_items.id
}

resource "google_bigquery_table" "thelook_ecommerce_inventory_items" {
  project     = var.project_id
  dataset_id  = "thelook_ecommerce"
  table_id    = "inventory_items"
  description = "Programatically generated inventory for The Look fictitious e-commerce store"
  depends_on = [
    google_bigquery_dataset.thelook_ecommerce
  ]
}

output "bigquery_table-thelook_ecommerce_inventory_items-table_id" {
  value = google_bigquery_table.thelook_ecommerce_inventory_items.table_id
}

output "bigquery_table-thelook_ecommerce_inventory_items-id" {
  value = google_bigquery_table.thelook_ecommerce_inventory_items.id
}

resource "google_bigquery_table" "thelook_ecommerce_distribution_centers" {
  project     = var.project_id
  dataset_id  = "thelook_ecommerce"
  table_id    = "distribution_centers"
  description = "The Look fictitious e-commerce dataset: distribution_centers table"
  depends_on = [
    google_bigquery_dataset.thelook_ecommerce
  ]
}

output "bigquery_table-thelook_ecommerce_distribution_centers-table_id" {
  value = google_bigquery_table.thelook_ecommerce_distribution_centers.table_id
}

output "bigquery_table-thelook_ecommerce_distribution_centers-id" {
  value = google_bigquery_table.thelook_ecommerce_distribution_centers.id
}
