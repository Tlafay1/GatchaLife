import { describe, it, expect, vi, beforeEach, type Mock } from 'vitest';
import { mount } from '@vue/test-utils';
import { ref } from 'vue';
import CharacterEditor from '@/character/views/CharacterEditor.vue';
import * as apiClient from '@/lib/api-client';
import { QueryClient, VueQueryPlugin } from '@tanstack/vue-query';
import type { Router } from 'vue-router';

vi.mock('@/lib/api-client');
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('CharacterEditor.vue', () => {
  const routerMock = {
    push: vi.fn(),
  } as unknown as Router;

  beforeEach(() => {
    vi.clearAllMocks();
    global.alert = vi.fn();

    // Mock the API client hooks
    (apiClient.useSeriesList as Mock).mockReturnValue({ data: [], isLoading: false });
    (apiClient.useCharacterDetails as Mock).mockReturnValue({ data: null, isLoading: false });
    (apiClient.useCreateSeries as Mock).mockReturnValue({ mutateAsync: vi.fn() });
    (apiClient.useCreateCharacter as Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
    (apiClient.useUpdateCharacter as Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
    (apiClient.useCreateVariant as Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
    (apiClient.useUpdateVariant as Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
    (apiClient.useDeleteVariant as Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
    (apiClient.useUploadVariantImage as Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
    (apiClient.useDeleteVariantImage as Mock).mockReturnValue({ mutateAsync: vi.fn(), isPending: ref(false) });
  });

  it('renders the form', () => {
    const wrapper = mount(CharacterEditor, {
      global: {
        plugins: [
          (app) => {
            const queryClient = new QueryClient();
            app.use(VueQueryPlugin, { queryClient });
            app.config.globalProperties.$router = routerMock;
          },
        ],
        stubs: {
          'router-link': true,
        }
      },
    });
    expect(wrapper.find('h1').text()).toContain('Character Forge');
  });

  it('submits the form and calls the correct API endpoints', async () => {
    const createCharacterMock = vi.fn().mockResolvedValue({ id: 1 });
    (apiClient.useCreateCharacter as Mock).mockReturnValue({ mutateAsync: createCharacterMock, isPending: ref(false) });

    const wrapper = mount(CharacterEditor, {
      global: {
        plugins: [
          (app) => {
            const queryClient = new QueryClient();
            app.use(VueQueryPlugin, { queryClient });
            app.config.globalProperties.$router = routerMock;
          },
        ],
        stubs: {
          'router-link': true,
        }
      },
    });

    // Fill out the form
    await wrapper.find('input[placeholder="e.g. Sylphiette"]').setValue('Test Character');
    await wrapper.find('textarea[placeholder="Core traits: species, gender, personality, key features..."]').setValue('Test Description');
    // Mock series selection
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (wrapper.vm as any).form.series = '1';

    // Submit the form
    await wrapper.find('button').trigger('click');

    // Assert that the createCharacter mutation was called with the correct data
    expect(createCharacterMock).toHaveBeenCalledWith({
      name: 'Test Character',
      series: 1,
      description: 'Test Description',
      unlock_level: 1
    });
  });
});
