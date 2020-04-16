variable "test_key" {
    type = string
}
output "test" {
    value = "${var.test_key}"
}
resource "null_resource" "test" {
}
