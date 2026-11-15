
resource "docker_image" "nginx" {
  name         = "nginx:alpine"
  keep_locally = true
}

resource "docker_container" "nginx" {
  name  = "sre-terraform-nginx"
  image = docker_image.nginx.image_id

  ports {
    internal = 80
    external = 8085
    ip       = "127.0.0.1"
  }

  networks_advanced {
    name = docker_network.sre_demo.name
  }

  volumes {
    volume_name    = docker_volume.sre_demo.name
    container_path = "/lab-data"
  }
}
