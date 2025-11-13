import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { apiService } from "@/services/api";
import { Category } from "@/types";

export function CategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async (): Promise<void> => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiService.getCategories();
      setCategories(data);
    } catch (err) {
      setError("Error al cargar las categorías");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Cargando categorías...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Categorías</h1>
        <Link
          to="/categories/new"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Crear Categoría
        </Link>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {categories.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <p className="text-gray-500 text-lg">
            No hay categorías disponibles. Crea tu primera categoría.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {categories.map((category) => (
            <div
              key={category.id}
              className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
            >
              {category.picture_url && (
                <div className="h-48 bg-gray-200 overflow-hidden">
                  <img
                    src={category.picture_url}
                    alt={category.name}
                    className="w-full h-full object-cover"
                  />
                </div>
              )}
              <div className="p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {category.name}
                </h3>
                {category.slug && (
                  <p className="text-sm text-gray-500 mb-2">
                    Slug: <span className="font-mono">{category.slug}</span>
                  </p>
                )}
                {category.description && (
                  <p className="text-gray-700 mb-4 line-clamp-3">
                    {category.description}
                  </p>
                )}
                <div className="flex justify-between items-center text-sm text-gray-500">
                  <span>
                    Creada: {new Date(category.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
