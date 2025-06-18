export interface ProductProps {
  id: string;
  imageUrl: string;
  name: string;
  price: number;
  originalPrice?: number;
  store: string;
  rating?: number;
  url: string;
  lastUpdated: string;
}

export const productList: ProductProps[] = [
 {
    id: "1",
    imageUrl: "https://images.tokopedia.net/img/cache/500-square/product-1/2020/7/7/9328291/9328291_8eaa5a0b-0b3e-4e3a-9a5f-3a3b3b3b3b3b.jpg",
    name: "Smartphone XYZ Pro 128GB",
    price: 4999000,
    originalPrice: 5499000,
    store: "Tokopedia",
    rating: 4.8,
    url: "https://tokopedia.link/example",
    lastUpdated: "2023-11-15"
  },
  {
    id: "2",
    imageUrl: "https://images.shopee.co.id/id/1111111111/1111111111_1111111111.jpg",
    name: "Laptop ABC Ultra Thin",
    price: 8999000,
    originalPrice: 9999000,
    store: "Shopee",
    rating: 4.5,
    url: "https://shopee.co.id/example",
    lastUpdated: "2023-11-14"
  },
  {
    id: "3",
    imageUrl: "https://images.bukalapak.com/img/11111111/original/data.jpeg",
    name: "Headphone Wireless Premium",
    price: 1299000,
    store: "Bukalapak",
    rating: 4.2,
    url: "https://bukalapak.com/example",
    lastUpdated: "2023-11-13"
  },
  {
    id: "4",
    imageUrl: "https://images.lazada.co.id/p/11111111/11111111.jpg",
    name: "Smart Watch Series 5",
    price: 2499000,
    originalPrice: 2999000,
    store: "Lazada",
    rating: 4.7,
    url: "https://lazada.co.id/example",
    lastUpdated: "2023-11-12"
  },
  {
    id: "5",
    imageUrl: "https://images.blibli.com/flyaway/files/product-images/11111111_11111111_11111111.jpg",
    name: "Tablet DEF 10 inch",
    price: 3499000,
    store: "Blibli",
    rating: 4.3,
    url: "https://blibli.com/example",
    lastUpdated: "2023-11-11"
  },
  {
    id: "6",
    imageUrl: "https://images.jd.id/11111111/11111111_11111111_11111111.jpg",
    name: "Kamera Mirrorless GH5",
    price: 12999000,
    originalPrice: 14999000,
    store: "JD.id",
    rating: 4.9,
    url: "https://jd.id/example",
    lastUpdated: "2023-11-10"
  },
  {
    id: "1",
    imageUrl: "https://images.tokopedia.net/img/cache/500-square/product-1/2020/7/7/9328291/9328291_8eaa5a0b-0b3e-4e3a-9a5f-3a3b3b3b3b3b.jpg",
    name: "Smartphone XYZ Pro 128GB",
    price: 4999000,
    originalPrice: 5499000,
    store: "Tokopedia",
    rating: 4.8,
    url: "https://tokopedia.link/example",
    lastUpdated: "2023-11-15"
  },
  {
    id: "2",
    imageUrl: "https://images.shopee.co.id/id/1111111111/1111111111_1111111111.jpg",
    name: "Laptop ABC Ultra Thin",
    price: 8999000,
    originalPrice: 9999000,
    store: "Shopee",
    rating: 4.5,
    url: "https://shopee.co.id/example",
    lastUpdated: "2023-11-14"
  },
];
