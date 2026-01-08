"use client";

import { motion } from "framer-motion";

export function ExperienceSection() {
    return (
        <section id="experience" className="py-64 sm:py-96 px-4 sm:px-6 lg:px-8 relative overflow-hidden bg-[var(--bg-primary)]">
            {/* Subtle top border */}
            <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-green-500/40 to-transparent" />

            <div className="flex justify-center">
                <div className="relative w-full max-w-3xl text-center">
                    {/* Section Header */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="mb-12"
                    >
                        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-green-500/10 border border-green-500/20 text-green-400 text-sm font-medium mb-6">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                            Experience
                        </span>
                        <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-[var(--text-primary)] mb-4">
                            Internship & <span className="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">Experience</span>
                        </h2>
                    </motion.div>

                    {/* Experience Card */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="relative text-left"
                    >
                        <div className="absolute -inset-[1px] rounded-2xl bg-gradient-to-r from-green-500 via-emerald-500 to-cyan-500 opacity-20" />

                        <div className="relative p-6 sm:p-8 bg-[var(--bg-card)] rounded-2xl border border-[var(--border-subtle)]">
                            {/* Header */}
                            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-5">
                                <div>
                                    <h3 className="text-xl sm:text-2xl font-bold text-[var(--text-primary)] mb-1">Software Development Intern</h3>
                                    <p className="text-base text-green-400 font-medium">SolutionAve</p>
                                </div>
                                <span className="px-3 py-1.5 bg-green-500/10 border border-green-500/20 text-green-400 text-sm font-medium rounded-full whitespace-nowrap self-start">
                                    2024
                                </span>
                            </div>

                            {/* Description */}
                            <p className="text-[var(--text-secondary)] mb-5 text-sm sm:text-base leading-relaxed">
                                Worked on production-grade software development, contributing to real-world projects and gaining hands-on experience with modern development workflows.
                            </p>

                            {/* Stack & Outcomes */}
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                                <div>
                                    <h4 className="text-xs font-semibold text-[var(--text-primary)] uppercase tracking-wider mb-2">Tech Stack</h4>
                                    <div className="flex flex-wrap gap-1.5">
                                        {["Flutter", "Dart", "REST APIs", "Firebase", "Git"].map((tech) => (
                                            <span key={tech} className="px-2.5 py-1 text-xs bg-[var(--bg-tertiary)] text-[var(--text-secondary)] rounded-md">
                                                {tech}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                                <div>
                                    <h4 className="text-xs font-semibold text-[var(--text-primary)] uppercase tracking-wider mb-2">Key Outcomes</h4>
                                    <ul className="space-y-1.5">
                                        {["Built production-ready features", "Integrated third-party APIs", "Collaborated in agile team"].map((outcome) => (
                                            <li key={outcome} className="flex items-start gap-2 text-xs text-[var(--text-tertiary)]">
                                                <svg className="w-3.5 h-3.5 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                                </svg>
                                                {outcome}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </div>

            {/* Subtle bottom border */}
            <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-green-500/40 to-transparent" />
        </section>
    );
}
