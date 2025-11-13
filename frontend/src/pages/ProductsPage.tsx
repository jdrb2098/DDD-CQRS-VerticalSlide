import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { apiService } from "@/services/api";
import { Product, ProductsQueryParams } from "@/types";

export function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 10,
    total_items: 0,
    total_pages: 0,
  });
  const [filters, setFilters] = useState<ProductsQueryParams>({
    page: 1,
    per_page: 10,
  });

  useEffect(() => {
    loadProducts();
  }, [filters]);

  const loadProducts = async (): Promise<void> => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiService.getProducts(filters);
      setProducts(response.items);
      setPagination({
        page: response.page,
        per_page: response.per_page,
        total_items: response.total_items,
        total_pages: response.total_pages,
      });
    } catch (err) {
      setError("Error al cargar los productos");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePageChange = (newPage: number): void => {
    setFilters((prev) => ({ ...prev, page: newPage }));
  };

  const handleFilterChange = (
    key: keyof ProductsQueryParams,
    value: string | number | boolean | undefined
  ): void => {
    setFilters((prev) => ({
      ...prev,
      [key]: value || undefined,
      page: 1,
    }));
  };

  if (isLoading && products.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Cargando productos...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Productos</h1>
        <Link
          to="/products/new"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Crear Producto
        </Link>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* Filters */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label
              htmlFor="name-filter"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Nombre
            </label>
            <input
              id="name-filter"
              type="text"
              value={filters.name || ""}
              onChange={(e) => handleFilterChange("name", e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="Buscar por nombre..."
            />
          </div>
          <div>
            <label
              htmlFor="available-filter"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Disponible
            </label>
            <select
              id="available-filter"
              value={
                filters.available === undefined
                  ? ""
                  : filters.available.toString()
              }
              onChange={(e) =>
                handleFilterChange(
                  "available",
                  e.target.value === "" ? undefined : e.target.value === "true"
                )
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="">Todos</option>
              <option value="true">Sí</option>
              <option value="false">No</option>
            </select>
          </div>
          <div>
            <label
              htmlFor="min-price-filter"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Precio Mínimo
            </label>
            <input
              id="min-price-filter"
              type="number"
              value={filters.min_price || ""}
              onChange={(e) =>
                handleFilterChange(
                  "min_price",
                  e.target.value ? parseFloat(e.target.value) : undefined
                )
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="0.00"
            />
          </div>
          <div>
            <label
              htmlFor="max-price-filter"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Precio Máximo
            </label>
            <input
              id="max-price-filter"
              type="number"
              value={filters.max_price || ""}
              onChange={(e) =>
                handleFilterChange(
                  "max_price",
                  e.target.value ? parseFloat(e.target.value) : undefined
                )
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="9999.99"
            />
          </div>
        </div>
      </div>

      {/* Products Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Nombre
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                SKU
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Precio
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Stock
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Disponible
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {products.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-6 py-4 text-center text-gray-500">
                  No se encontraron productos
                </td>
              </tr>
            ) : (
              products.map((product) => (
                <tr key={product.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {product.id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {product.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {product.sku}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${product.price.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {product.units_in_stock}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        product.available
                          ? "bg-green-100 text-green-800"
                          : "bg-red-100 text-red-800"
                      }`}
                    >
                      {product.available ? "Sí" : "No"}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <Link
                      to={`/products/${product.id}/edit`}
                      className="text-blue-600 hover:text-blue-900"
                    >
                      Editar
                    </Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {pagination.total_pages > 1 && (
        <div className="mt-6 flex items-center justify-between">
          <div className="text-sm text-gray-700">
            Mostrando {(pagination.page - 1) * pagination.per_page + 1} a{" "}
            {Math.min(
              pagination.page * pagination.per_page,
              pagination.total_items
            )}{" "}
            de {pagination.total_items} productos
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => handlePageChange(pagination.page - 1)}
              disabled={pagination.page === 1}
              className="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              Anterior
            </button>
            <span className="px-4 py-2 text-sm text-gray-700">
              Página {pagination.page} de {pagination.total_pages}
            </span>
            <button
              onClick={() => handlePageChange(pagination.page + 1)}
              disabled={pagination.page >= pagination.total_pages}
              className="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              Siguiente
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
