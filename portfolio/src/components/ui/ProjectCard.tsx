"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Project } from "@/types";
import { getLanguageColor, formatRelativeTime } from "@/lib/github";

interface ProjectCardProps {
    project: Project;
    index?: number;
}

export function ProjectCard({ project, index = 0 }: ProjectCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            whileHover={{ y: -8 }}
            className="group h-full"
        >
            <Link href={`/projects/${project.slug}`} className="block h-full">
                <div className="relative h-full bg-gradient-to-br from-[var(--bg-card)] to-[var(--bg-secondary)] rounded-2xl border border-[var(--border-subtle)] hover:border-violet-500/30 transition-all duration-500 overflow-hidden">
                    {/* Gradient Overlay on Hover */}
                    <div className="absolute inset-0 bg-gradient-to-br from-violet-500/5 to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

                    {/* Top Gradient Line */}
                    <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-violet-500 via-purple-500 to-cyan-500 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

                    {/* Content */}
                    <div className="relative p-6 flex flex-col h-full">
                        {/* Header */}
                        <div className="flex items-start justify-between gap-4 mb-4">
                            {/* Icon */}
                            <div className="p-3 bg-gradient-to-br from-violet-500/10 to-purple-500/10 rounded-xl border border-violet-500/20">
                                <svg className="w-6 h-6 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                                </svg>
                            </div>

                            {/* Stars */}
                            {project.stars > 0 && (
                                <div className="flex items-center gap-1 px-2 py-1 bg-[var(--bg-tertiary)] rounded-lg">
                                    <svg className="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                    </svg>
                                    <span className="text-sm font-medium text-[var(--text-secondary)]">{project.stars}</span>
                                </div>
                            )}
                        </div>

                        {/* Title */}
                        <h3 className="text-lg font-semibold text-[var(--text-primary)] group-hover:text-violet-400 transition-colors mb-2 line-clamp-1">
                            {project.title || project.name.replace(/-/g, " ")}
                        </h3>

                        {/* Description */}
                        <p className="text-sm text-[var(--text-tertiary)] line-clamp-2 mb-4 flex-grow">
                            {project.customDescription || project.description || "A project in my portfolio. Click to learn more."}
                        </p>

                        {/* Topics */}
                        {project.topics && project.topics.length > 0 && (
                            <div className="flex flex-wrap gap-2 mb-4">
                                {project.topics.slice(0, 3).map((topic) => (
                                    <span
                                        key={topic}
                                        className="px-2 py-1 text-xs bg-[var(--bg-tertiary)] text-[var(--text-secondary)] rounded-md"
                                    >
                                        {topic}
                                    </span>
                                ))}
                                {project.topics.length > 3 && (
                                    <span className="px-2 py-1 text-xs text-[var(--text-muted)]">
                                        +{project.topics.length - 3}
                                    </span>
                                )}
                            </div>
                        )}

                        {/* Footer */}
                        <div className="flex items-center justify-between pt-4 border-t border-[var(--border-subtle)]">
                            {/* Language */}
                            {project.language && (
                                <div className="flex items-center gap-2">
                                    <span
                                        className="w-3 h-3 rounded-full"
                                        style={{ backgroundColor: getLanguageColor(project.language) }}
                                    />
                                    <span className="text-sm text-[var(--text-secondary)]">{project.language}</span>
                                </div>
                            )}

                            {/* Updated */}
                            <span className="text-xs text-[var(--text-muted)]">
                                {formatRelativeTime(project.updatedAt)}
                            </span>
                        </div>
                    </div>

                    {/* Hover Arrow */}
                    <div className="absolute bottom-6 right-6 w-8 h-8 rounded-full bg-violet-500/10 flex items-center justify-center opacity-0 group-hover:opacity-100 transform translate-x-4 group-hover:translate-x-0 transition-all duration-300">
                        <svg className="w-4 h-4 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                        </svg>
                    </div>
                </div>
            </Link>
        </motion.div>
    );
}

/**
 * Skeleton loader for ProjectCard
 */
export function ProjectCardSkeleton() {
    return (
        <div className="bg-gradient-to-br from-[var(--bg-card)] to-[var(--bg-secondary)] rounded-2xl border border-[var(--border-subtle)] p-6">
            <div className="flex items-start justify-between mb-4">
                <div className="skeleton w-12 h-12 rounded-xl" />
                <div className="skeleton w-12 h-6 rounded-lg" />
            </div>
            <div className="skeleton h-6 w-3/4 mb-2 rounded-lg" />
            <div className="skeleton h-4 w-full mb-1 rounded" />
            <div className="skeleton h-4 w-2/3 mb-4 rounded" />
            <div className="flex gap-2 mb-4">
                <div className="skeleton h-6 w-16 rounded-md" />
                <div className="skeleton h-6 w-16 rounded-md" />
            </div>
            <div className="pt-4 border-t border-[var(--border-subtle)] flex justify-between">
                <div className="skeleton h-4 w-20 rounded" />
                <div className="skeleton h-4 w-16 rounded" />
            </div>
        </div>
    );
}
