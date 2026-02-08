// GST Rate Mapping for Popular HSN Codes
// Updated: February 2026

const gstRates = {
  // Electronics - 18%
  "8471": "18%",  // Computers, laptops
  "8517": "18%",  // Mobile phones
  "8528": "18%",  // TV
  "8443": "18%",  // Printers
  "8518": "18%",  // Headphones, speakers
  "8504": "18%",  // Chargers, adapters
  "8507": "28%",  // Power banks (batteries)
  "8523": "18%",  // USB drives, memory cards
  
  // Vehicles
  "8703": "28%",  // Cars
  "8711": "28%",  // Motorcycles, scooters
  "8712": "12%",  // Bicycles
  "8704": "28%",  // Trucks
  "4011": "28%",  // Tyres
  
  // Food - 0% (unprocessed), 5% (some), 12-18% (processed)
  "1006": "0%",   // Rice
  "1001": "0%",   // Wheat
  "1101": "5%",   // Flour
  "1701": "5%",   // Sugar
  "2501": "5%",   // Salt
  "1507": "5%",   // Soybean oil
  "1512": "5%",   // Sunflower oil
  "1511": "5%",   // Palm oil
  "0401": "0%",   // Fresh milk
  "0402": "5%",   // Milk powder
  "0405": "12%",  // Butter, ghee
  "0406": "12%",  // Cheese, paneer
  "0902": "5%",   // Tea
  "0901": "5%",   // Coffee
  "1905": "18%",  // Biscuits (0% for plain bread)
  
  // Clothing - 5% (cotton), 12% (general), 18% (branded)
  "6205": "12%",  // Men's shirts
  "6206": "12%",  // Women's shirts
  "6109": "12%",  // T-shirts
  "6203": "12%",  // Trousers
  "6204": "12%",  // Women's trousers
  "5208": "5%",   // Saree (cotton)
  "6110": "12%",  // Sweaters
  "6201": "12%",  // Jackets
  
  // Footwear - 5% (under ₹500), 18% (over ₹500)
  "6403": "18%",  // Leather shoes
  "6404": "12%",  // Canvas shoes
  "6402": "12%",  // Sandals, chappals
  "6401": "18%",  // Boots
  
  // Furniture - 18%
  "9403": "18%",  // Tables, beds, cupboards
  "9401": "18%",  // Chairs, sofas
  "9404": "18%",  // Mattresses
  
  // Appliances - 18% or 28%
  "8418": "28%",  // Refrigerators
  "8415": "28%",  // Air conditioners
  "8450": "28%",  // Washing machines
  "8414": "18%",  // Fans
  "8516": "18%",  // Geysers, water heaters, irons
  "8509": "18%",  // Mixers, grinders
  
  // Personal Care - 18% or 28%
  "3401": "18%",  // Soap
  "3305": "28%",  // Shampoo
  "3306": "18%",  // Toothpaste, toothbrush
  "3304": "28%",  // Creams, lotions
  
  // Stationery - 12% or 18%
  "9608": "18%",  // Pens
  "9609": "12%",  // Pencils
  "4820": "12%",  // Notebooks
  "4901": "0%",   // Books (printed)
  
  // Construction - 12% or 28%
  "2523": "28%",  // Cement
  "6901": "12%",  // Bricks
  "6907": "18%",  // Tiles
  "3208": "18%",  // Paint
  
  // Jewelry - 3%
  "7113": "3%",   // Gold, silver jewelry
  
  // Medicine - 12%
  "3004": "12%",  // Medicines (tablets)
  "3003": "12%",  // Medicine (syrup)
  "3002": "12%"   // Injections
};

// Function to get GST rate for HSN code
function getGSTRate(hsnCode) {
  // Try exact match
  if (gstRates[hsnCode]) {
    return gstRates[hsnCode];
  }
  
  // Try matching shorter codes (8471 matches 847130, 847140 etc)
  for (let code in gstRates) {
    if (hsnCode.startsWith(code)) {
      return gstRates[code];
    }
  }
  
  return null; // No rate found
}
