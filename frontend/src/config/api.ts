// In production, use the environment variable
// In development, use the direct API URL
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  (import.meta.env.DEV ? "http://localhost:8000" : "http://localhost:8000");

export const API_ENDPOINTS = {
  AUTH: {
    TOKEN: "/auth/token",
  },
  PRODUCTS: {
    LIST: "/products",
    CREATE: "/products",
    BULK: "/products/bulk",
  },
  CATEGORIES: {
    LIST: "/categories",
    BY_ID: (id: number) => `/categories/${id}`,
  },
} as const;
