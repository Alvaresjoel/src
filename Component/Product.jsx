export default function Product({product}){
  if (!product) {
    return null;
  }
  return (
    <>
      <h2>{product.title}</h2>
      <h3>{product.price}</h3>
      {product.category && <h3>{product.category}</h3>}
      <h3>{product.description}</h3>
    </>
  )
}