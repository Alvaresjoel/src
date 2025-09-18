import { NavLink, useNavigate } from 'react-router-dom';
import { getAuthToken } from '../utils/auth';
function NavBar(){
    const navigate = useNavigate();
    const isAuthed = !!getAuthToken();

    function handleLogout(){
        localStorage.removeItem('token');
        navigate('/login');
    }

    return(
        <nav>
            <ul>
                {!isAuthed && (
                    <>
                    <li>
                    <NavLink to='/'>
                        Home
                    </NavLink>
                    </li>
                    <li>
                        <NavLink to='/login'>
                            Login
                        </NavLink>
                    </li>
                    </>
                )}
                {isAuthed && (
                    <>
                    <li>
                        <NavLink to='/add-product'>
                            Add Product
                        </NavLink>
                    </li>
                    <li>
                        <button onClick={handleLogout}>Logout</button>
                    </li>
                    </>
                )}
            </ul>
        </nav>
    )


}

export default NavBar