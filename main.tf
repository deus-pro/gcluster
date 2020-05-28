terraform {
  backend "remote" {
    organization = "deus"
    workspaces {
      name = "gcluster"
    }
  }
}
variable "cloud_key" {
  type = string
}
resource "null_resource" "test" {
}
provider "google" {
  credentials = var.cloud_key
  project     = "samuel-test-00"
  region      = "us-central1"
  version     = "~> 3.17.0"
}
resource "google_container_cluster" "primary" {
  provider                 = google
  name                     = "dojo-gke-cluster"
  location                 = "us-central1"
  remove_default_node_pool = true
  initial_node_count       = 1
  release_channel {
    channel = "RAPID"
  }
}
resource "google_container_node_pool" "primary_preemptible_nodes" {
  name     = "dojo-node-pool"
  location = "us-central1"
  cluster  = google_container_cluster.primary.name
  autoscaling {
    min_node_count = 0
    max_node_count = 3
  }
  node_config {
    preemptible  = true
    machine_type = "n1-standard-1"
    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}
