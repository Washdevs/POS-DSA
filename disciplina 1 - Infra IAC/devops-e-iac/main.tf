provider "aws" {
  region  = "us-east-2"  
}

resource "aws_instance" "tarefa1" {
  ami           = "ami-05df0ea761147eda6"  # AMI na AWS
  instance_type = "t2.micro"

  tags = {
    Name = "processador-virtual" #Identificação da Instância
  }
}
