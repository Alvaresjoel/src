import { Outlet } from "react-router-dom";
import NavBar from "../Component/NavigationBar";

function RootLayout(){

    return (
        <>  
        <NavBar/> 
            <main>
                    <Outlet/>
            </main>
        </>
    )


}

export default RootLayout