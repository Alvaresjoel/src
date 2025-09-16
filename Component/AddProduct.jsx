import { useActionState, useContext } from "react"
import { useNavigate } from "react-router-dom"
import { ProductContext } from "../store/ProductContext"
import Submit from "./Submit"
export default function AddProduct(){
    const navigate = useNavigate();
    const { addProduct: addProductToContext } = useContext(ProductContext);

    async function addProduct(prevState,formData){
        const productName = formData.get('productName')
        const productPrice = formData.get('productPrice')
        const productQuantity = formData.get('productQuantity')
        const productDescription = formData.get('productDescription')
        let errors = []

        if (productName.trim().length < 5){
            errors.push('Invalid product')
        }
        if(productPrice < 0){
            errors.push('Product price cannot be negative')
        }
        if( productQuantity < 0){
            errors.push('Product quantity cannot be negative')
        }

        if (errors.length > 0) {
            return{errors,productValues:{
                productName,
                productPrice,
                productQuantity,
                productDescription
            }}
        }

        const newProduct = {
            title: productName,
            price: Number(productPrice),
            quantity: Number(productQuantity),
            description: productDescription
        };
        addProductToContext(newProduct);
        navigate('/products');
        return {errors:null}

    }

    const [formState,formAction] = useActionState(addProduct,{errors:null})
    
    return(

        <form action={formAction}>
            <h2>Enter Product Details</h2>
            <div className="control-row">
                <div className="control">
                    <label htmlFor="Product Name">Product Name</label>
                    <input  type="text" name="productName" id="product_name" defaultValue={formState.productValues?.productName} />
                </div>
            </div>
            <div className="control-row">
                <div className="control">
                    <label htmlFor="Product Description">Product Description</label>
                    <textarea type="text" name="productDescription" id="product_description" defaultValue={formState.productValues?.productDescription} />                    
                </div>
            </div>

            <div className="control-row">
                <div className="control">
                    <label htmlFor="Product Quantity">Product Quantity</label>
                    <input type="text" name="productQuantity" id="product_quantity" defaultValue={formState.productValues?.productQuantity} />                    
                </div>
            </div>
            
            <div className="control-row">
                <div className="control">
                    <label htmlFor="Product Price">Product Price</label>
                    <input type="text" name="productPrice" id="product_price" defaultValue={formState.productValues?.productPrice}/>                    
                </div>
            </div>
            <Submit/>
        </form>
    )
}