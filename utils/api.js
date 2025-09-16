// const url = "http://localhost:8000"

export async function getProducts(){
    // const response = DUMMY_PRODUCTS
    
    // if (!response.ok){
    //     throw new Error('Failed to fetch products')   
    // }
      return Promise.resolve(DUMMY_PRODUCTS);

}

const DUMMY_PRODUCTS = [
    {id:'p1', title:'Product 1', description:'This is product 1', price:6},
    {id:'p2', title:'Product 2', description:'This is product 2', price:7},
    {id:'p3', title:'Product 3', description:'This is product 3', price:8}
]