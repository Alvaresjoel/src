import Products from "../pages/Products"
import { ProductContextProvider } from "../store/ProductContextProvider"
function Home(){
    return(
        <>
            <ProductContextProvider>
                <Products/>
            </ProductContextProvider>
        </>
    )

}

export default Home



