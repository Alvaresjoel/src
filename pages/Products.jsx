import { useContext, useEffect } from "react";
import { ProductContext } from "../store/ProductContext";
import Product from "../Component/Product";

export default function Products() {
  const { products, fetchProducts } = useContext(ProductContext);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]); // add fetchProducts to deps

  return (
    <div>
      <h2>Products</h2>
      {products.length === 0 && <p>No products yet.</p>}
      <ul className="product-list">
        {products.map((product) => (
          <li key={product.id}>
            <Product product={product} />
          </li>
        ))}
      </ul>
    </div>
  );
}
