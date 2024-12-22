class AddressError(Exception):
  """Custom exception for address errors in the Distance Matrix API."""
  def __init__(self, address_type):
    super().__init__(f"Invalid {address_type} address.")
    self.address_type = address_type