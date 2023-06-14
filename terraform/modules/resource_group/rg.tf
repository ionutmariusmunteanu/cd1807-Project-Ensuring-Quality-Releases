resource "azurerm_resource_group" "test" {
  name     = "${var.resource_group}"
  location = "${var.resource_group_location}"
}
