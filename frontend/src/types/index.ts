export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface Product {
  id: number;
  name: string;
  sku: string;
  description: string | null;
  quantity_per_unit: string | null;
  units_in_stock: number;
  units_on_order: number;
  discontinued: boolean;
  price: number;
  available: boolean;
  category_id: number | null;
  created_by_user_id: number | null;
  created_at: string;
  updated_at: string | null;
}

export interface ProductCreateRequest {
  name: string;
  sku: string; // El controlador espera slug, no sku directamente
  description?: string;
  price: number;
  stock: number; // El controlador espera stock (requerido), no units_in_stock
  category_id?: number;
}

export interface ProductUpdateRequest extends Partial<ProductCreateRequest> {
  id: number;
}

export interface ProductsResponse {
  items: Product[];
  page: number;
  per_page: number;
  total_items: number;
  total_pages: number;
}

export interface ProductsQueryParams {
  page?: number;
  per_page?: number;
  name?: string;
  category_id?: number;
  available?: boolean;
  discontinued?: boolean;
  min_price?: number;
  max_price?: number;
}

export interface Category {
  id: number;
  name: string;
  slug: string | null;
  description: string | null;
  picture_url: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface CategoryCreateRequest {
  name: string;
  slug?: string;
  description?: string;
  picture?: File;
}

export interface ApiError {
  detail: string | { message: string };
}
