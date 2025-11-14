import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { ref } from 'vue';
import CharacterEditor from '@/character/views/CharacterEditor.vue';
import * as apiClient from '@/lib/api-client';

vi.mock('@/lib/api-client');

describe('CharacterEditor.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();

    // Mock the API client hooks
    (apiClient.useSeriesList as vi.Mock).mockReturnValue({ data: [], isLoading: false });
    (apiClient.useCharacterDetails as vi.Mock).mockReturnValue({ data: null, isLoading: false });
    (apiClient.useCreateSeries as vi.Mock).mockReturnValue({ mutateAsync: vi.fn() });
    (apiClient.useCreateCharacter as vi.Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
    (apiClient.useUpdateCharacter as vi.Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
    (apiClient.useCreateVariant as vi.Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
    (apiClient.useUpdateVariant as vi.Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
    (apiClient.useDeleteVariant as vi.Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
    (apiClient.useUploadVariantImage as vi.Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
    (apiClient.useDeleteVariantImage as vi.Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
  });

  it('renders the form', () => {
    const wrapper = mount(CharacterEditor, {
      global: {
        plugins: [
          // Provide a mock router
          {
            install: (app) => {
              app.config.globalProperties.$router = {
                push: vi.fn(),
              };
            },
          },
          // Provide Vue Query client
           (app) => {
            const queryClient = new (require('@tanstack/vue-query').QueryClient)();
            app.use(require('@tanstack/vue-query').VueQueryPlugin, { queryClient });
          },
        ],
        stubs: {
          'router-link': true,
        }
      },
    });
    expect(wrapper.find('h1').text()).toContain('Character Forge');
  });
});
