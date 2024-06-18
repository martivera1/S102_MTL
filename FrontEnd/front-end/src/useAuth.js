import { useState, useEffect } from 'react';
import { BACKEND_URL } from '../src/constants';

export const useAuth = () => {
    const [user, setUser] = useState(null);
    const [error, setError] = useState(null);
  
    useEffect(() => {
      const fetchUser = async () => {
        try {
          const response = await fetch(`${BACKEND_URL}/api/user_info`);
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          setUser(data.email); // Set user directly to email string
          console.log("data from call in react: " + data.email);
        } catch (error) {
          setError(error.message);
          console.error('Error fetching user info:', error);
        }
      };
  
      fetchUser();
    }, []);
  
    return user; // Return email string or null
};
