import { cva, type VariantProps } from 'class-variance-authority'

export { default as Navbar } from './Navbar.vue'
export { default as NavbarContent } from './NavbarContent.vue'
export { default as NavbarLinks } from './NavbarLinks.vue'
export { default as NavbarLink } from './NavbarLink.vue'

export const navbarVariants = cva(
  `block w-full mx-auto top-0 z-50 bg-primary
  dark:bg-primary dark:has-[a]:text-primary-foreground`,
  {
    variants: {
      variant: {
        default: 'text-primary-foreground shadow-md sticky',
        dark: 'text-primary-foreground bg-primary',
        transparent: 'bg-transparent shadow-none has-[a]:text-2xl has-[a]:text-primary-foreground'
      },
      size: {
        default: 'px-4 py-2 lg:px-8 lg:py-3',
        lg: 'px-4 py-4 lg:px-8 lg:py-6'
      }
    },
    defaultVariants: {
      variant: 'transparent',
      size: 'default'
    }
  }
)

export type NavbarVariants = VariantProps<typeof navbarVariants>
