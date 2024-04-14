resource "null_resource" "deploy_docker_compose" {
  provisioner "local-exec" {
    command = "docker-compose up -d"
    working_dir = "."
  }
}

resource "null_resource" "save_images" {
    depends_on = [null_resource.deploy_docker_compose]

    provisioner "local-exec"{
        command = "docker save -o db_my_web_app_docker_image.tar postgres"
        working_dir = "."
    }

    provisioner "local-exec"{
        command = "docker save -o task_manager.tar task_manager"
        working_dir = "."
    }
}
