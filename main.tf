variable "cloud_key" {
    type = string
}
resource "null_resource" "test" {
}
provider "google" {
  credentials = "${var.cloud_key}"
  project     = "samuel-test-00"
  region      = "us-central1"
  version     = "~> 3.12.0"
}
resource "google_container_cluster" "primary" {
  name     = "dojo-gke-cluster"
  location = "us-central1"
  remove_default_node_pool = true
  initial_node_count       = 1
}
resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "dojo-node-pool"
  location   = "us-central1"
  cluster    = google_container_cluster.primary.name
  node_count = 1
  node_config {
    preemptible  = true
    machine_type = "n1-standard-1"
    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}
