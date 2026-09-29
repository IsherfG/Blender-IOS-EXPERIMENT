// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://shlok-bhakta.github.io',
	base: '/3d-modeling-thingy-ios',
	publicDir: '../docs-media',
	integrations: [
		starlight({
			title: 'Blender for iOS',
			description: 'Install and use Blender 5.2 on iPhone and iPad.',
			social: [
				{
					icon: 'github',
					label: 'GitHub',
					href: 'https://github.com/Shlok-Bhakta/3d-modeling-thingy-ios',
				},
			],
			sidebar: [
				{ label: 'Start here', items: [{ label: 'Overview', slug: 'index' }, { label: 'Install', slug: 'install' }] },
				{
					label: 'Controls',
					items: [
						{ label: 'Touch and gestures', slug: 'controls/touch' },
						{ label: 'Keyboard, mouse, and Pencil', slug: 'controls/keyboard-mouse-pencil' },
					],
				},
				{
					label: 'Workflows',
					items: [
						{ label: 'Files and windows', slug: 'workflow/files-and-windows' },
						{ label: 'Rendering', slug: 'workflow/rendering' },
					],
				},
				{ label: 'Reference', items: [{ label: 'What is different', slug: 'what-is-different' }, { label: 'Known limitations', slug: 'limitations' }] },
			],
		}),
	],
});
