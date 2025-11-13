import { API_BASE_URL } from "@/config/api";
import {
  ApiError,
  Category,
  CategoryCreateRequest,
  LoginCredentials,
  Product,
  ProductCreateRequest,
  ProductsQueryParams,
  ProductsResponse,
  TokenResponse,
} from "@/types";
import { storage } from "@/utils/storage";
import axios, {
  AxiosError,
  AxiosInstance,
  InternalAxiosRequestConfig,
} from "axios";

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        "Content-Type": "application/json",
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor - Add token to headers
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = storage.getToken();
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error: AxiosError) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor - Handle 401 errors
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiError>) => {
        if (error.response?.status === 401) {
          storage.removeToken();
          if (window.location.pathname !== "/login") {
            window.location.href = "/login";
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const formData = new URLSearchParams();
    formData.append("username", credentials.username);
    formData.append("password", credentials.password);

    const response = await this.client.post<TokenResponse>(
      "/auth/token",
      formData,
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );
    return response.data;
  }

  // Product endpoints
  async getProducts(params?: ProductsQueryParams): Promise<ProductsResponse> {
    const response = await this.client.get<ProductsResponse>("/products", {
      params,
    });
    return response.data;
  }

  async createProduct(data: ProductCreateRequest): Promise<Product> {
    const response = await this.client.post<Product>("/products", data);
    return response.data;
  }

  // Category endpoints
  async getCategories(): Promise<Category[]> {
    const response = await this.client.get<Category[]>("/categories");
    return response.data;
  }

  async getCategoryById(id: number): Promise<Category> {
    const response = await this.client.get<Category>(`/categories/${id}`);
    return response.data;
  }

  async createCategory(data: CategoryCreateRequest): Promise<Category> {
    // El controlador espera: name (requerido), slug (opcional),
    // description (opcional), picture (opcional)
    const formData = new FormData();
    formData.append("name", data.name);

    if (data.slug) formData.append("slug", data.slug);
    if (data.description) formData.append("description", data.description);
    if (data.picture) formData.append("picture", data.picture);

    const response = await this.client.post<Category>("/categories", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  }
}

export const apiService = new ApiService();
