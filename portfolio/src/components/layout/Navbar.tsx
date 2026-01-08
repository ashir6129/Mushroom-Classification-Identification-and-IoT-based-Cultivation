"use client";

import { motion } from "framer-motion";
import Image from "next/image";

const navItems = [
    { name: "About", href: "#about" },
    { name: "Projects", href: "#projects" },
    { name: "Skills", href: "#skills" },
    { name: "Experience", href: "#experience" },
    { name: "Contact", href: "#contact" },
];

export function Navbar() {
    const scrollToSection = (e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
        e.preventDefault();
        const element = document.querySelector(href);
        if (element) {
            element.scrollIntoView({ behavior: "smooth" });
        }
    };

    return (
        <nav className="fixed top-0 left-0 right-0 z-50">
            <div className="backdrop-blur-xl bg-[var(--bg-primary)]/80 border-b border-[var(--border-subtle)]">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        {/* Logo */}
                        <a
                            href="#hero"
                            onClick={(e) => scrollToSection(e, "#hero")}
                            className="flex items-center gap-2"
                        >
                            <motion.span
                                whileHover={{ scale: 1.05 }}
                                className="text-xl font-bold bg-gradient-to-r from-violet-400 to-cyan-400 bg-clip-text text-transparent"
                            >
                                MAK
                            </motion.span>
                        </a>

                        {/* Desktop Navigation */}
                        <div className="hidden md:flex items-center gap-1">
                            {navItems.map((item) => (
                                <a
                                    key={item.name}
                                    href={item.href}
                                    onClick={(e) => scrollToSection(e, item.href)}
                                    className="px-4 py-2 text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors rounded-lg hover:bg-[var(--bg-card)]"
                                >
                                    {item.name}
                                </a>
                            ))}
                            <a
                                href="#contact"
                                onClick={(e) => scrollToSection(e, "#contact")}
                                className="ml-4 px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-violet-600 to-purple-600 rounded-lg hover:shadow-lg hover:shadow-violet-500/25 transition-all"
                            >
                                Get in Touch
                            </a>
                        </div>

                        {/* Mobile Menu Button */}
                        <MobileMenu />
                    </div>
                </div>
            </div>
        </nav>
    );
}

function MobileMenu() {
    const [isOpen, setIsOpen] = React.useState(false);

    const scrollToSection = (href: string) => {
        setIsOpen(false);
        const element = document.querySelector(href);
        if (element) {
            element.scrollIntoView({ behavior: "smooth" });
        }
    };

    return (
        <>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="md:hidden p-2 hover:bg-[var(--bg-card)] rounded-lg transition-colors"
                aria-label="Toggle menu"
            >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    {isOpen ? (
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    ) : (
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    )}
                </svg>
            </button>

            {isOpen && (
                <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="absolute top-full left-0 right-0 md:hidden backdrop-blur-xl bg-[var(--bg-primary)]/95 border-b border-[var(--border-subtle)]"
                >
                    <div className="px-4 py-4 space-y-1">
                        {navItems.map((item) => (
                            <a
                                key={item.name}
                                href={item.href}
                                onClick={() => scrollToSection(item.href)}
                                className="block px-4 py-3 text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)] rounded-lg transition-colors"
                            >
                                {item.name}
                            </a>
                        ))}
                    </div>
                </motion.div>
            )}
        </>
    );
}

import React from "react";
