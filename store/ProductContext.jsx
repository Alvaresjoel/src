import { createContext } from "react";
export const ProductContext = createContext({
    products:[],
    fetchProducts: () => {},
    addProduct: () => {}
})