terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.6"
    }
  }
}

provider "docker" {}

resource "docker_network" "sre_demo" {
  name = "sre-terraform-demo-network"
}

resource "docker_volume" "sre_demo" {
  name = "sre-terraform-demo-data"
}

output "network_name" {
  value = docker_network.sre_demo.name
}

output "volume_name" {
  value = docker_volume.sre_demo.name
}