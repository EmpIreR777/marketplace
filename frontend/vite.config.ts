import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
    plugins: [vue(), vueJsx(), vueDevTools()],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
        },
    },
    css: {
        preprocessorOptions: {
            scss: {
                additionalData: `@use "vuetify/styles"; @use "@/scss/_vars.scss" as *;  @use "@/scss/_breakpoints.scss" as *; @use "@/scss/_typography.scss" as *;`,
            },
        },
    },
    server: {
        host: '0.0.0.0',  // чтобы слушал не только localhost
        port: 5173,
        fs: {
            allow: ['..'], // Разрешить доступ к родительским директориям
        },
    },
})
// server: {  // Для локального запуска через Docker
//     host: true, // слушать все интерфейсы
//         port: 5173,
//             strictPort: true, // завершить если порт занят
//                 hmr: {
//         clientPort: 5173 // важно для HMR в Docker
//     }
// },