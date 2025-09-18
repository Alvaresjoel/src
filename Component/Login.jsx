import { useActionState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import {
  isEmail,
  isNotEmpty,
  isEqualToOtherValue,
  hasMinLength,
} from '../utils/validation.js';

function LoginAction(prevFormState, formData) {

  return { errors: null, success: true };
}

export default function Login() {
  const navigate = useNavigate();
  const [formState, formAction] = useActionState(LoginAction, {
    errors: [],
    success: false,
  });

  useEffect(() => {
    if (formState?.success) {
      localStorage.setItem('token', 'demo-token');
      navigate('/products');
    }
  }, [formState?.success, navigate]);

  return (
    <form action={formAction}>

    <div className="control-row">
      <div className="control">
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          name="email"
          defaultValue={formState.enteredValues?.email}
        />
      </div>

        <div className="control">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            name="password"
            defaultValue={formState.enteredValues?.password}
          />
        </div>
        </div>

        

      {formState.errors && (
        <ul className="error">
          {formState.errors.map((error) => (
            <li key={error}>{error}</li>
          ))}
        </ul>
      )}

      <p className="form-actions">
        <button type="reset" className="button button-flat">
          Reset
        </button>
        <button className="button">Login</button>
      </p>
    </form>
  );
}