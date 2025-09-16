import { useActionState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import {
  isEmail,
  isNotEmpty,
  isEqualToOtherValue,
  hasMinLength,
} from '../utils/validation.js';

function LoginAction(prevFormState, formData) {
  const email = formData.get('email');
  const password = formData.get('password');
//   const confirmPassword = formData.get('confirm-password');
//   const firstName = formData.get('first-name');
//   const lastName = formData.get('last-name');
//   const role = formData.get('role');

  let errors = [];

  if (!isEmail(email)) {
    errors.push('Invalid email address.');
  }

  if (!isNotEmpty(password) || !hasMinLength(password, 6)) {
    errors.push('You must provide a password with at least six characters.');
  }

//   if (!isEqualToOtherValue(password, confirmPassword)) {
//     errors.push('Passwords do not match.');
//   }

//   if (!isNotEmpty(firstName) || !isNotEmpty(lastName)) {
//     errors.push('Please provide both your first and last name.');
//   }

//   if (!isNotEmpty(role)) {
//     errors.push('Please select a role.');
//   }

  if (errors.length > 0) {
    return {
      errors,
      enteredValues: {
        email,
        password,
        // confirmPassword,
        // firstName,
        // lastName,
        // role,
      },
    };
  }

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
      <h2>Welcome on board!</h2>
      <p>We just need a little bit of data from you to get you started 🚀</p>

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