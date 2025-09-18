
import './App.css'
import Header from './Component/Header.jsx'
import AddProductPage from './pages/AddProductPage.jsx'
import Products from './pages/Products.jsx'
import RequireAuth from './routes/RequireAuth.jsx'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import RootLayout from './pages/Root.jsx'
import Home from './pages/Home.jsx'
import LoginPage from './pages/LoginPage.jsx'

const router = createBrowserRouter([
{
  path:'/',
  element:<RootLayout/>,
  children:[
      {index:true,element:<Home/>},
      {path:'login',element:<LoginPage/>},
      {path:'add-product',element:<AddProductPage/>,loader:RequireAuth},
  ] 
}

])

function App() {

  return (
    <>
      <Header/>
      <main>
          <RouterProvider router={router}/>
      </main>
    </>
  )
}

export default App
