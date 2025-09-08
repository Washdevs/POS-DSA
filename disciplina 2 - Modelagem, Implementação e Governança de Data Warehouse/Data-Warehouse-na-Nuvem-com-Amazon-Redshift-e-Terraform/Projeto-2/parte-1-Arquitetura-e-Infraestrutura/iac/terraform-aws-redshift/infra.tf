provider "aws" {
    region = "us-east-2"
}

resource "aws_vpc" "redshift_vpc" { # "recurso" "nome do meu recurso"
  cidr_block = "10.0.0.0/16" # Range de endereços IPS para esta VPC
 
  tags = {
    Name = "DSA redshift_vpc" # Descrição
  }
}

