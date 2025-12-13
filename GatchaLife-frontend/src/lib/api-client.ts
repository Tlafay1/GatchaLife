import { OpenAPI, SeriesService, CharactersService, VariantsService, VariantImagesService, StylesService, ThemesService, RaritiesService } from '@/api';
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
    mutationFn: ({ id, ...data }: { id: number, name: string, description?: string, unlock_level?: number }) =>
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
    mutationFn: ({ id, ...data }: { id: number, name: string, series: number, description?: string, unlock_level?: number }) =>
      CharactersService.charactersUpdate(id, data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['characters'] });
      queryClient.invalidateQueries({ queryKey: ['character', data.id] });
    },
  });
};

export const useUploadCharacterFace = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: { characterId: number; file: File; }) => {
      const formData = new FormData();
      formData.append('identity_face_image', data.file);
      const response = await fetch(`${OpenAPI.BASE}/characters/${data.characterId}/`, {
        method: 'PATCH',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Image upload failed');
      }
      return response.json();
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['character', data.id] });
      queryClient.invalidateQueries({ queryKey: ['characters'] });
    },
  });
};

export const useGenerateCharacter = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: { characterId: number; wiki_text: string }) => {
      // Reuse the create endpoint logic or a specific update-from-profile logic?
      // The user wants to "regenerate from scratch by AI like creation".
      // Usually this means calling the same profiling logic but on an existing character.
      // CharacterViewSet.create handles creating from wiki_text.
      // CharacterViewSet.update doesn't seem to have special wiki_text handling in the provided code, 
      // but let's assume we can POST to a custom action or just use update if modified.
      // Actually, looking at views.py (from memory/context), perform_create handles wiki_source_text.
      // If we want to re-run it on existing character, we probably need a custom action 'regenerate' or similar,
      // OR we just use the 'update' passing wiki_text if the backend supports it.
      // Let's assume we need a new action or reuse creation logic.
      // WAIT, the user asked to "create frontend to regenerate".
      // If I look at views.py, `perform_update` might not have the AI logic.
      // Let's check views.py content again if I could? No, I must rely on memory or what I see.
      // I saw `perform_create` having the AI logic. `perform_update` was not explicitly shown with AI logic.
      // I'll add a new action `regenerate_profile` in backend in next step if needed, but for now let's define the hook
      // to call an endpoint I WILL create: POST /characters/{id}/regenerate_profile/

      const response = await fetch(`${OpenAPI.BASE}/characters/${data.characterId}/regenerate_from_wiki/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wiki_source_text: data.wiki_text }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error || 'Failed to regenerate character');
      }
      return response.json();
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['character', variables.characterId] });
    },
  });
};

export const useCreateVariants = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: { characterId: number; prompt?: string }) => {
      const response = await fetch(`${OpenAPI.BASE}/characters/${data.characterId}/create-variants/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: data.prompt }),
      });
      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error || 'Failed to create variants');
      }
      return response.json();
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['character', variables.characterId] });
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
    mutationFn: ({ id, ...data }: { id: number, name: string, description?: string, character: number }) =>
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
  return useMutation({
    mutationFn: (id: number) => VariantImagesService.variantImagesDelete(id),
    onSuccess: () => {
      // Invalidation will be handled by the calling component
    },
  });
};

// --- Rarities ---
export const useRaritiesList = () => useQuery({
  queryKey: ['rarities'],
  queryFn: () => RaritiesService.raritiesList(),
});

// --- Styles ---
export const useStylesList = () => useQuery({
  queryKey: ['styles'],
  queryFn: () => StylesService.stylesList(),
});

export const useCreateStyle = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: StylesService.stylesCreate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['styles'] });
    },
  });
};

export const useUpdateStyle = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...data }: { id: number, name: string, style_keywords?: string, composition_hint?: string, rarity: number }) =>
      StylesService.stylesUpdate(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['styles'] });
    },
  });
};

export const useDeleteStyle = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => StylesService.stylesDelete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['styles'] });
    },
  });
};

// --- Themes ---
export const useThemesList = () => useQuery({
  queryKey: ['themes'],
  queryFn: () => ThemesService.themesList(),
});

export const useCreateTheme = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ThemesService.themesCreate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['themes'] });
    },
  });
};

export const useUpdateTheme = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...data }: {
      id: number,
      name: string,
      category?: string,
      ambiance?: string,
      keywords_theme?: string,
      prompt_background?: string,
      integration_idea?: string,
      unlock_level?: number
    }) =>
      ThemesService.themesUpdate(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['themes'] });
    },
  });
};

export const useDeleteTheme = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => ThemesService.themesDelete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['themes'] });
    },
  });
};
// --- Gamification ---
export const usePlayerStats = () => useQuery({
  queryKey: ['player'],
  queryFn: async () => {
    const response = await fetch(`${OpenAPI.BASE}/gamification/player/`);
    if (!response.ok) throw new Error('Failed to fetch player stats');
    // The viewset returns a list, but we want the first item (singleton player)
    // Actually, the viewset logic I wrote returns a list for ModelViewSet unless we use a specific action or ID.
    // Wait, my backend viewset `PlayerViewSet` is a ModelViewSet. `get_object` is overridden but `list` still returns a list.
    // I should probably just fetch the list and take the first one, or use a specific endpoint.
    // Let's assume I'll fix the backend or just handle the list here.
    // For simplicity in this "single user" app, let's just fetch the list and take the first one.
    const data = await response.json();
    return Array.isArray(data) ? data[0] : data;
  },
});

export const useSyncTickTick = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      const response = await fetch(`${OpenAPI.BASE}/gamification/player/sync_ticktick/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      });
      if (!response.ok) throw new Error('Sync failed');
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['player'] });
    },
  });
};

export const useQuestsList = () => useQuery({
  queryKey: ['quests'],
  queryFn: async () => {
    const response = await fetch(`${OpenAPI.BASE}/gamification/quests/`);
    if (!response.ok) throw new Error('Failed to fetch quests');
    return response.json();
  },
});

export const useClaimQuest = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      const response = await fetch(`${OpenAPI.BASE}/gamification/quests/${id}/claim/`, {
        method: 'POST',
      });
      if (!response.ok) throw new Error('Claim failed');
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['player'] });
      queryClient.invalidateQueries({ queryKey: ['quests'] });
    },
  });
};

import { unref, type Ref } from 'vue';

export const useCollection = (filters?: Ref<Record<string, unknown>> | Record<string, unknown>) => useQuery({
  queryKey: ['collection', filters],
  queryFn: async () => {
    const params = new URLSearchParams(unref(filters) as Record<string, string>);
    const response = await fetch(`${OpenAPI.BASE}/gamification/collection/?${params}`);
    if (!response.ok) throw new Error('Failed to fetch collection');
    return response.json();
  },
});

export const useCardDetails = (id: number) => useQuery({
  queryKey: ['card', id],
  queryFn: async () => {
    const response = await fetch(`${OpenAPI.BASE}/gamification/collection/${id}/`);
    if (!response.ok) throw new Error('Failed to fetch card details');
    return response.json();
  },
  enabled: !!id,
});

export const useCardPreview = (params: Record<string, string>) => useQuery({
  queryKey: ['card_preview', params],
  queryFn: async () => {
    const query = new URLSearchParams(params);
    const response = await fetch(`${OpenAPI.BASE}/gamification/collection/preview/?${query.toString()}`);
    if (!response.ok) throw new Error('Failed to fetch card preview');
    return response.json();
  },
  enabled: !!params.variant_id && !!params.rarity,
});

export const useRerollCardImage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      const response = await fetch(`${OpenAPI.BASE}/gamification/collection/${id}/reroll_image/`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Reroll failed');
      }
      return response.json();
    },
    onSuccess: (data, id) => {
      queryClient.setQueryData(['card', id], data); // Optimistic update or just set data
      queryClient.invalidateQueries({ queryKey: ['card', id] });
      queryClient.invalidateQueries({ queryKey: ['collection'] });
    },
  });
};

export const useGatchaRoll = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      console.log('Sending roll request to', `${OpenAPI.BASE}/gamification/gatcha/roll/`);
      const response = await fetch(`${OpenAPI.BASE}/gamification/gatcha/roll/`, {
        method: 'POST',
      });
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Roll failed', response.status, errorText);
        throw new Error(`Roll failed: ${response.status} ${errorText}`);
      }
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['player'] });
      queryClient.invalidateQueries({ queryKey: ['collection'] });
    },
  });
};

export const useTickTickStats = () => useQuery({
  queryKey: ['ticktick-stats'],
  queryFn: async () => {
    const response = await fetch(`${OpenAPI.BASE}/ticktick/stats/`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  },
});

export const useTaskHistory = (page = 1, pageSize = 20) => useQuery({
  queryKey: ['ticktick-history', page, pageSize],
  queryFn: async () => {
    const response = await fetch(`${OpenAPI.BASE}/ticktick/history/?page=${page}&page_size=${pageSize}`);
    if (!response.ok) throw new Error('Failed to fetch history');
    return response.json();
  },
});

export const useProgressionStats = () => useQuery({
  queryKey: ['ticktick-progression'],
  queryFn: async () => {
    const response = await fetch(`${OpenAPI.BASE}/ticktick/progression/`);
    if (!response.ok) throw new Error('Failed to fetch progression');
    return response.json();
  },
});
