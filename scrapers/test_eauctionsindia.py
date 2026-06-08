from eauctionsindia import (
    search_eauctionsindia_goa
)

data = search_eauctionsindia_goa()

print(f"\nTotal Records: {len(data)}\n")

if data:
    print(data[0])