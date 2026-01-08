"use client";

import { motion } from "framer-motion";

export function AboutSection() {
    return (
        <section id="about" className="py-64 sm:py-96 px-4 sm:px-6 lg:px-8 relative overflow-hidden bg-[var(--bg-secondary)]">
            {/* Subtle top border */}
            <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-violet-500/40 to-transparent" />

            {/* Background glow */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-violet-500/5 rounded-full blur-3xl" />

            <div className="flex justify-center">
                <div className="relative w-full max-w-4xl text-center">
                    {/* Section Header */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="mb-12"
                    >
                        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-400 text-sm font-medium mb-6">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                            About Me
                        </span>
                        <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-[var(--text-primary)] mb-4">
                            My <span className="bg-gradient-to-r from-violet-400 to-cyan-400 bg-clip-text text-transparent">Mindset</span>
                        </h2>
                    </motion.div>

                    {/* Quote */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6, delay: 0.1 }}
                        className="mb-10"
                    >
                        <blockquote className="text-xl sm:text-2xl md:text-3xl font-medium text-[var(--text-primary)] leading-relaxed max-w-3xl mx-auto">
                            &ldquo;I believe skills are learnable. With strong fundamentals, I adapt to any technology, domain, or challenge.&rdquo;
                        </blockquote>
                    </motion.div>

                    {/* Description */}
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                        className="text-[var(--text-secondary)] text-lg leading-relaxed max-w-2xl mx-auto mb-12"
                    >
                        As a Computer Science student at FAST NUCES, I&apos;ve built a strong foundation in algorithms, systems, and software engineering. But what defines me isn&apos;t just what I know — it&apos;s my ability to learn what I don&apos;t.
                    </motion.p>

                    {/* Traits Grid */}
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl mx-auto">
                        {[
                            { icon: "🧠", title: "Strong CS Foundation" },
                            { icon: "🔄", title: "Adaptability" },
                            { icon: "💡", title: "Curiosity" },
                            { icon: "🎯", title: "Problem Solver" },
                        ].map((trait, i) => (
                            <motion.div
                                key={trait.title}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.4, delay: 0.1 * i }}
                                className="p-4 bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl hover:border-violet-500/30 transition-colors"
                            >
                                <span className="text-2xl mb-2 block">{trait.icon}</span>
                                <h3 className="text-sm font-medium text-[var(--text-primary)]">{trait.title}</h3>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Subtle bottom border */}
            <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-violet-500/40 to-transparent" />
        </section>
    );
}
