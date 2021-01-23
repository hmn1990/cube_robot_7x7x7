#include <linux/build-salt.h>
#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(.gnu.linkonce.this_module) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section(__versions) = {
	{ 0x45cd1b70, "module_layout" },
	{ 0xa43edd50, "device_destroy" },
	{ 0xedc03953, "iounmap" },
	{ 0xc6b71c2b, "cdev_del" },
	{ 0x6091b333, "unregister_chrdev_region" },
	{ 0xdb3c72dc, "class_destroy" },
	{ 0xca42ba96, "device_create" },
	{ 0xf7c80868, "__class_create" },
	{ 0x196792f, "cdev_add" },
	{ 0xe3ec2f2b, "alloc_chrdev_region" },
	{ 0x18e84c7b, "cdev_init" },
	{ 0xf31c6384, "cdev_alloc" },
	{ 0x1d37eeed, "ioremap" },
	{ 0xbb72d4fe, "__put_user_1" },
	{ 0xdecd0b29, "__stack_chk_fail" },
	{ 0xc5850110, "printk" },
	{ 0xf76b0a59, "read_current_timer" },
	{ 0x5f754e5a, "memset" },
	{ 0xbcab6ee6, "sscanf" },
	{ 0x28118cb6, "__get_user_1" },
	{ 0x8f678b07, "__stack_chk_guard" },
	{ 0xd697e69a, "trace_hardirqs_on" },
	{ 0x8e865d3c, "arm_delay_ops" },
	{ 0xec3d2e1b, "trace_hardirqs_off" },
	{ 0x2c3c9134, "try_module_get" },
	{ 0xbe25f0d7, "module_put" },
	{ 0xb1ad28e0, "__gnu_mcount_nc" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "BFDC9F978DCD07C2A7D02DA");
