// User-Friendly Search Keywords → HSN Code Mapping
// This makes your technical database searchable with common terms

const searchKeywords = {
  // Electronics & Computers
  'laptop': ['8471'],
  'computer': ['8471'],
  'desktop': ['8471'],
  'pc': ['8471'],
  'notebook': ['8471'],
  'macbook': ['8471'],
  'chromebook': ['8471'],
  
  'mobile': ['8517'],
  'phone': ['8517'],
  'smartphone': ['8517'],
  'iphone': ['8517'],
  'android': ['8517'],
  'cellphone': ['8517'],
  'handset': ['8517'],
  
  'tablet': ['8471', '8517'],
  'ipad': ['8471'],
  
  'tv': ['8528'],
  'television': ['8528'],
  'led tv': ['8528'],
  'lcd tv': ['8528'],
  'smart tv': ['8528'],
  
  'printer': ['8443'],
  'scanner': ['8443'],
  'photocopier': ['8443'],
  
  'headphone': ['8518'],
  'earphone': ['8518'],
  'earbuds': ['8518'],
  'airpods': ['8518'],
  
  'speaker': ['8518'],
  'bluetooth speaker': ['8518'],
  
  'charger': ['8504'],
  'mobile charger': ['8504'],
  'adapter': ['8504'],
  'power bank': ['8507'],
  
  'pendrive': ['8523'],
  'usb drive': ['8523'],
  'flash drive': ['8523'],
  'memory card': ['8523'],
  
  // Vehicles
  'car': ['8703'],
  'sedan': ['8703'],
  'suv': ['8703'],
  'hatchback': ['8703'],
  'vehicle': ['8703'],
  
  'bike': ['8711'],
  'motorcycle': ['8711'],
  'scooter': ['8711'],
  'two wheeler': ['8711'],
  
  'bicycle': ['8712'],
  'cycle': ['8712'],
  
  'truck': ['8704'],
  'lorry': ['8704'],
  
  'tyre': ['4011'],
  'tire': ['4011'],
  
  // Food & Beverages
  'rice': ['1006'],
  'basmati': ['1006'],
  'wheat': ['1001'],
  'atta': ['1101'],
  'flour': ['1101'],
  'maida': ['1101'],
  
  'sugar': ['1701'],
  'salt': ['2501'],
  'oil': ['1507', '1512', '1511'],
  'cooking oil': ['1507'],
  'sunflower oil': ['1512'],
  'palm oil': ['1511'],
  
  'milk': ['0401', '0402'],
  'butter': ['0405'],
  'ghee': ['0405'],
  'cheese': ['0406'],
  'paneer': ['0406'],
  
  'tea': ['0902'],
  'coffee': ['0901'],
  
  'biscuit': ['1905'],
  'bread': ['1905'],
  'cake': ['1905'],
  
  // Clothing
  'shirt': ['6205', '6206'],
  'tshirt': ['6109'],
  't-shirt': ['6109'],
  'trouser': ['6203', '6204'],
  'pant': ['6203'],
  'jeans': ['6203'],
  
  'saree': ['5208'],
  'dress': ['6204'],
  'kurta': ['6206'],
  
  'sweater': ['6110'],
  'jacket': ['6201'],
  
  // Footwear
  'shoes': ['6403', '6404'],
  'sandal': ['6402'],
  'chappal': ['6402'],
  'slipper': ['6402'],
  'boots': ['6401'],
  
  // Home & Furniture
  'furniture': ['9403'],
  'sofa': ['9401'],
  'chair': ['9401'],
  'table': ['9403'],
  'bed': ['9403'],
  'mattress': ['9404'],
  
  // Appliances
  'fridge': ['8418'],
  'refrigerator': ['8418'],
  'ac': ['8415'],
  'air conditioner': ['8415'],
  'washing machine': ['8450'],
  'fan': ['8414'],
  'geyser': ['8516'],
  'water heater': ['8516'],
  'mixer': ['8509'],
  'grinder': ['8509'],
  
  // Personal Care
  'soap': ['3401'],
  'shampoo': ['3305'],
  'toothpaste': ['3306'],
  'toothbrush': ['3306'],
  'cream': ['3304'],
  'lotion': ['3304'],
  
  // Stationery
  'pen': ['9608'],
  'pencil': ['9609'],
  'notebook': ['4820'],
  'copy': ['4820'],
  'book': ['4901'],
  
  // Construction
  'cement': ['2523'],
  'brick': ['6901'],
  'tiles': ['6907'],
  'paint': ['3208'],
  
  // Jewelry
  'gold': ['7113'],
  'silver': ['7113'],
  'jewelry': ['7113'],
  'jewellery': ['7113'],
  
  // Medicine
  'medicine': ['3004'],
  'tablet': ['3004'],
  'syrup': ['3003'],
  'injection': ['3002']
};

// Function to find HSN codes from user query
function findHSNFromKeyword(query) {
  const lowerQuery = query.toLowerCase().trim();
  
  // Check exact match
  if (searchKeywords[lowerQuery]) {
    return searchKeywords[lowerQuery];
  }
  
  // Check partial match
  for (let keyword in searchKeywords) {
    if (lowerQuery.includes(keyword) || keyword.includes(lowerQuery)) {
      return searchKeywords[keyword];
    }
  }
  
  return null;
}
