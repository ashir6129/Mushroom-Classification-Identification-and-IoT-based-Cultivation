"use client";

import { motion } from "framer-motion";
import { Project } from "@/types";
import { getLanguageColor, formatRelativeTime } from "@/lib/github";
import { useState } from "react";
import { ProjectModal } from "../ui/ProjectModal";

interface ProjectsSectionProps {
    projects: Project[];
}

export function ProjectsSection({ projects }: ProjectsSectionProps) {
    const [selectedProject, setSelectedProject] = useState<Project | null>(null);

    const sortedProjects = [...projects].sort((a, b) =>
        b.stars - a.stars || new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
    );

    return (
        <section id="projects" className="py-64 sm:py-96 px-4 sm:px-6 lg:px-8 relative overflow-hidden bg-[var(--bg-primary)]">
            {/* Subtle top border */}
            <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />

            {/* Background glow */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-cyan-500/5 rounded-full blur-3xl" />

            <div className="flex justify-center">
                <div className="relative w-full max-w-6xl text-center">
                    {/* Section Header */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="mb-12"
                    >
                        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-sm font-medium mb-6">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                            </svg>
                            Auto-synced from GitHub
                        </span>
                        <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-[var(--text-primary)] mb-4">
                            Computer Science <span className="bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">Projects</span>
                        </h2>
                        <p className="text-lg text-[var(--text-secondary)] max-w-xl mx-auto">
                            Real projects built with real technologies, automatically synced from my GitHub.
                        </p>
                    </motion.div>

                    {/* Projects Grid */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                        {sortedProjects.map((project, index) => (
                            <motion.button
                                key={project.id}
                                onClick={() => setSelectedProject(project)}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.5, delay: index * 0.05 }}
                                whileHover={{ y: -6 }}
                                className="group block text-left w-full"
                            >
                                <div className="relative h-full w-full bg-[var(--bg-card)] rounded-2xl border border-[var(--border-subtle)] hover:border-cyan-500/30 transition-all duration-300 overflow-hidden p-5">
                                    {/* Top accent line */}
                                    <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-cyan-500 via-blue-500 to-violet-500 opacity-0 group-hover:opacity-100 transition-opacity" />

                                    {/* Header */}
                                    <div className="flex items-start justify-between gap-3 mb-3">
                                        <div className="p-2.5 bg-cyan-500/10 rounded-lg border border-cyan-500/20">
                                            <svg className="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                                            </svg>
                                        </div>
                                        {project.stars > 0 && (
                                            <div className="flex items-center gap-1 px-2 py-1 bg-[var(--bg-tertiary)] rounded-md">
                                                <svg className="w-3.5 h-3.5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                                                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                                </svg>
                                                <span className="text-xs font-medium text-[var(--text-secondary)]">{project.stars}</span>
                                            </div>
                                        )}
                                    </div>

                                    {/* Title */}
                                    <h3 className="text-base font-semibold text-[var(--text-primary)] group-hover:text-cyan-400 transition-colors mb-2 line-clamp-1">
                                        {project.name.replace(/-/g, " ")}
                                    </h3>

                                    {/* Description */}
                                    <p className="text-sm text-[var(--text-tertiary)] line-clamp-2 mb-3">
                                        {project.description || "A project in my portfolio."}
                                    </p>

                                    {/* Footer */}
                                    <div className="flex items-center justify-between pt-3 border-t border-[var(--border-subtle)]">
                                        {project.language && (
                                            <div className="flex items-center gap-1.5">
                                                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: getLanguageColor(project.language) }} />
                                                <span className="text-xs text-[var(--text-secondary)]">{project.language}</span>
                                            </div>
                                        )}
                                        <span className="text-xs text-[var(--text-muted)]">{formatRelativeTime(project.updatedAt)}</span>
                                    </div>
                                </div>
                            </motion.button>
                        ))}
                    </div>

                    {/* GitHub Link */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6, delay: 0.3 }}
                        className="mt-10"
                    >
                        <a
                            href="https://github.com/ashir6129"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-2 px-5 py-2.5 bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] text-[var(--text-primary)] text-sm font-medium rounded-lg border border-[var(--border-light)] hover:border-cyan-500/50 transition-all"
                        >
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                            </svg>
                            View All on GitHub
                        </a>
                    </motion.div>
                </div>
            </div>

            {/* Modal */}
            <ProjectModal
                project={selectedProject}
                onClose={() => setSelectedProject(null)}
            />

            {/* Subtle bottom border */}
            <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />
        </section>
    );
}
