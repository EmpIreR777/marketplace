import type { IBaseQueryParams } from '@/api/models'
import { DEFAULT_LIMIT } from '@/enums/httpEnum'
import type { InfiniteScrollStatus } from '@/types/index'
import { reactive } from 'vue'

interface InfiniteLoaderState {
  count: number
  offset: number
  limit: number
  loadedCount: number
}

interface InfiniteLoaderParams<T> {
  loader: (params: IBaseQueryParams) => Promise<{ results: T[]; count: number }>
  params?: IBaseQueryParams
}

interface InfiniteLoaderScrollParams {
  loader: () => Promise<{ status: InfiniteScrollStatus }>
  done: (status: InfiniteScrollStatus) => void
}

interface InfinitLoaderComposition {
  loadData: <T>(
    args: InfiniteLoaderParams<T>,
  ) => Promise<{ status: InfiniteScrollStatus; data?: T[] }>
  loadOnScroll: (args: InfiniteLoaderScrollParams) => Promise<void>
  resetLoader: () => void
  state: InfiniteLoaderState
}

export function useInfiniteLoader(): InfinitLoaderComposition {
  const state = reactive<InfiniteLoaderState>({
    count: 0,
    offset: 0,
    limit: DEFAULT_LIMIT,
    loadedCount: 0,
  })

  async function loadData<T>({
    loader,
    params,
  }: InfiniteLoaderParams<T>): Promise<{ status: InfiniteScrollStatus; data?: T[] }> {
    if (state.loadedCount >= state.count && state.count !== 0) {
      return { status: 'empty' }
    }

    const defaultParams = {
      offset: state.offset,
      limit: state.limit,
      ...params,
    }
    let errorCount = 0

    while (errorCount < 2) {
      try {
        const response = await loader(defaultParams)

        if (Array.isArray(response) || !response.results.length) {
          return { status: 'empty' }
        }

        state.count = response.count
        state.offset += state.limit
        state.loadedCount += response.results.length

        return { status: 'ok', data: response.results }
      } catch (error) {
        errorCount++
        console.error('Ошибка при загрузке данных:', error)
        if (errorCount >= 2) {
          return { status: 'error' }
        }
      }
    }
    return { status: 'error' }
  }

  async function loadOnScroll({ loader, done }: InfiniteLoaderScrollParams): Promise<void> {
    try {
      const { status } = await loader()
      done(status)
    } catch (error) {
      console.error('Ошибка при загрузке данных на скролл:', error)
      done('error')
    }
  }

  function resetLoader() {
    state.count = 0
    state.offset = 0
    state.limit = DEFAULT_LIMIT
    state.loadedCount = 0
  }

  return {
    loadData,
    loadOnScroll,
    resetLoader,
    state,
  }
}
