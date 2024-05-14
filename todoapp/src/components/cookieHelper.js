// cookieHelper.js

import Cookies from 'js-cookie';

// Function to set a cookie
export const setCookie = (name, value, options = {}) => {
  Cookies.set(name, value, options);
};

// Function to get a cookie
export const getCookie = (name) => {
  return Cookies.get(name);
};

// Function to remove a cookie
export const removeCookie = (name) => {
  Cookies.remove(name);
};
