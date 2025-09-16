import {  useState, useCallback } from "react";
import { getProducts } from "../utils/api";
import { ProductContext } from "./ProductContext";

export function ProductContextProvider({children}){
    const [products,setProducts] = useState([]);
    const fetchProducts = useCallback(async () => {
        const products = await getProducts();
        setProducts(products);
    }, []);

    const addProduct = useCallback((newProduct) => {
        setProducts((prev) => {
            const productWithId = newProduct.id ? newProduct : { ...newProduct, id: `p${prev.length + 1}` };
            return [...prev, productWithId];
        });
    }, []);

    const productContext = {
        products: products,
        fetchProducts: fetchProducts,
        addProduct: addProduct
    }
    return  <ProductContext.Provider value={productContext}>{children}</ProductContext.Provider>
}