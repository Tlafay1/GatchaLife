import { OpenAPI, SeriesService, CharactersService, VariantsService, VariantImagesService } from '@/api';
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';

// Configure the base URL for the API client
OpenAPI.BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

// --- Series ---
export const useSeriesList = () => useQuery({
  queryKey: ['series'],
  queryFn: SeriesService.seriesList,
});

export const useCreateSeries = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: SeriesService.seriesCreate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['series'] });
    },
  });
};

export const useDeleteCharacter = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => CharactersService.charactersDelete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['characters'] });
    },
  });
};

export const useUpdateSeries = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...data }: { id: number, name: string, description?: string }) =>
      SeriesService.seriesUpdate(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['series'] });
    },
  });
};

export const useDeleteSeries = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => SeriesService.seriesDelete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['series'] });
    },
  });
};

// --- Characters ---
export const useCharactersList = () => useQuery({
  queryKey: ['characters'],
  queryFn: () => CharactersService.charactersList(),
});

export const useCharacterDetails = (id: number) => useQuery({
  queryKey: ['character', id],
  queryFn: () => CharactersService.charactersRead(id),
  enabled: !!id,
});

export const useCreateCharacter = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: CharactersService.charactersCreate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['characters'] });
    },
  });
};

export const useUpdateCharacter = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...data }: { id: number, name: string, series: number, description?: string }) =>
      CharactersService.charactersUpdate(id, data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['characters'] });
      queryClient.invalidateQueries({ queryKey: ['character', data.id] });
    },
  });
};

// --- Variants ---
export const useCreateVariant = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: VariantsService.variantsCreate,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['character', data.character] });
    },
  });
};

export const useUpdateVariant = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...data }: { id: number, name: string, description: string }) =>
      VariantsService.variantsUpdate(id, data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['character', data.character] });
    },
  });
};

export const useDeleteVariant = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id }: { id: number, characterId: number }) => VariantsService.variantsDelete(id),
    onSuccess: (data, { characterId }) => {
      queryClient.invalidateQueries({ queryKey: ['character', characterId] });
    },
  });
};

// --- Variant Images ---
export const useUploadVariantImage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: { variantId: number; file: File; }) => {
      const formData = new FormData();
      formData.append('variant', String(data.variantId));
      formData.append('image', data.file);

      const response = await fetch(`${OpenAPI.BASE}/variant-images/`, {
        method: 'POST',
        body: formData,
        // Let the browser set the Content-Type header
      });

      if (!response.ok) {
        throw new Error('Image upload failed');
      }
      return response.json();
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['character', data.variant] });
    },
  });
};

export const useDeleteVariantImage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => VariantImagesService.variantImagesDelete(id),
    onSuccess: () => {
      // Invalidation will be handled by the calling component
    },
  });
};
