resource "azurerm_network_interface" "test" {
  name                = "${var.application_type}-${var.resource_type}-NI"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group}"

  ip_configuration {
    name                          = "internal"
    subnet_id                     = "${var.subnet_id}"
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = "${var.public_ip}"
  }
}

resource "azurerm_linux_virtual_machine" "test" {
  name                = "${var.application_type}-${var.resource_type}"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group}"
  size                = "Standard_DS2_v2"
  admin_username      = "azureDevOps"
  network_interface_ids = [azurerm_network_interface.test.id]
  admin_ssh_key {
    username   = "azureDevOps"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDk/ibfJgffN/APLolfkP2f5VFKlppF7mjCcSY+6wNkA9LKeY3Y0/TWBlUDHDiX5pVcRxDBWXt4CMhDCYiP94DEsci3Ma7Jo27ZFtXQ3yjJtEGO3oDQ9nkDRMj5YTX4MXGgnNa85QuaanlaoAFtIcVWT73vIl0XmpmSXOOmoGoWly2+wnqbglQgrp6ZdLsmI3Me0UEudTsDxvrzfBm+w+e/UFgNN0Agjqxwd/I18zXx8ttp9xPr25siUyjv0fuhWrP2CQX8p++iSIGiqSS3SKMumHkzCBA5XGLHZk+cv65a9OAFQBT5FgQZGbDfx8enNpcF7dE/LgdRZdvzP2TeX32Fvt5dEXu+ONx7Kg99jAls+pQDcg1CTstlcQ4HrDteNOhXPb+HpCrtbIufClOp4EDLKqPlxDuz2QwNvSEHx79QP2KOVzu5cU0/6qASZRbIk9RxhQHldIGasc0ST3Ublpx1+nsmolvUd1G8hKXpKZGcYfmYtv+BzvKLLels6NNJxMM= BGROUP+MUNT043@BGPF3J0LQC"
  }
  os_disk {
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}
