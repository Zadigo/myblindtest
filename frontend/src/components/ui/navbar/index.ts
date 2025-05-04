import { cva, type VariantProps } from 'class-variance-authority'

export { default as Navbar } from './Navbar.vue'
export { default as NavbarContent } from './NavbarContent.vue'
export { default as NavbarLinks } from './NavbarLinks.vue'
export { default as NavbarLink } from './NavbarLink.vue'

export const navbarVariants = cva(
  `block w-full mx-auto top-0 z-50
  dark:bg-gray-800 dark:has-[a]:text-white`,
  {
    variants: {
      variant: {
        default: 'text-white bg-white shadow-md sticky',
        dark: 'text-white bg-slate-700'
      },
      size: {
        default: 'px-4 py-2 lg:px-8 lg:py-3',
        lg: 'px-4 py-4 lg:px-8 lg:py-6'
      }
    },
    defaultVariants: {
      variant: 'default',
      size: 'default'
    }
  }
)

export type NavbarVariants = VariantProps<typeof navbarVariants>
