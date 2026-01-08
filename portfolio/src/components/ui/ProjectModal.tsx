"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Project } from "@/types";
import { useEffect } from "react";
import { getLanguageColor } from "@/lib/github";

interface ProjectModalProps {
    project: Project | null;
    onClose: () => void;
}

export function ProjectModal({ project, onClose }: ProjectModalProps) {
    // Disable scroll when modal is open
    useEffect(() => {
        if (project) {
            document.body.style.overflow = "hidden";
        } else {
            document.body.style.overflow = "unset";
        }
        return () => {
            document.body.style.overflow = "unset";
        };
    }, [project]);

    if (!project) return null;

    return (
        <AnimatePresence>
            <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 md:p-10">
                {/* Backdrop */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={onClose}
                    className="absolute inset-0 bg-black/80 backdrop-blur-sm"
                />

                {/* Modal Content */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.9, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.9, y: 20 }}
                    className="relative w-full max-w-4xl max-h-[90vh] bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-3xl shadow-2xl overflow-hidden flex flex-col"
                >
                    {/* Close Button */}
                    <button
                        onClick={onClose}
                        className="absolute top-4 right-4 z-10 p-2 bg-black/20 hover:bg-black/40 rounded-full text-white/70 hover:text-white transition-colors"
                    >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>

                    <div className="overflow-y-auto custom-scrollbar">
                        {/* Header Image Placeholder / Media Section */}
                        <div className="relative w-full h-48 sm:h-64 md:h-80 bg-gradient-to-br from-violet-600/20 via-cyan-500/20 to-blue-600/20 flex items-center justify-center border-b border-[var(--border-subtle)]">
                            <div className="text-center p-6">
                                <div className="p-4 bg-white/5 rounded-2xl backdrop-blur-md border border-white/10 mb-4 inline-block">
                                    <svg className="w-12 h-12 text-violet-400 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <p className="text-sm text-[var(--text-tertiary)] font-medium">Project media (images/videos) coming soon</p>
                            </div>

                            {/* Project Icon Overlay */}
                            <div className="absolute -bottom-6 left-8 p-4 bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-2xl shadow-xl">
                                <div className="p-3 bg-violet-500/10 rounded-xl">
                                    <svg className="w-8 h-8 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                                    </svg>
                                </div>
                            </div>
                        </div>

                        {/* Content */}
                        <div className="p-8 pt-12">
                            <div className="flex flex-wrap items-center gap-3 mb-6">
                                <h2 className="text-2xl sm:text-3xl font-bold text-[var(--text-primary)]">
                                    {project.name.replace(/-/g, " ")}
                                </h2>
                                {project.stars > 0 && (
                                    <div className="flex items-center gap-1.5 px-3 py-1 bg-yellow-500/10 text-yellow-500 border border-yellow-500/20 rounded-full text-sm font-bold">
                                        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                        </svg>
                                        {project.stars}
                                    </div>
                                )}
                            </div>

                            <div className="space-y-8">
                                {/* Description */}
                                <div>
                                    <h3 className="text-sm font-bold text-[var(--text-muted)] uppercase tracking-widest mb-3">Project Overview</h3>
                                    <p className="text-[var(--text-secondary)] text-lg leading-relaxed">
                                        {project.description || "A comprehensive computer science project showcasing technical problem-solving and modern development practices."}
                                    </p>
                                </div>

                                {/* Tech Stack */}
                                <div>
                                    <h3 className="text-sm font-bold text-[var(--text-muted)] uppercase tracking-widest mb-3">Technologies Used</h3>
                                    <div className="flex flex-wrap gap-2">
                                        {project.language && (
                                            <div className="flex items-center gap-2 px-3 py-1.5 bg-[var(--bg-tertiary)] border border-[var(--border-subtle)] rounded-lg">
                                                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: getLanguageColor(project.language) }} />
                                                <span className="text-sm font-medium text-[var(--text-primary)]">{project.language}</span>
                                            </div>
                                        )}
                                        {/* Future implementation: tags from Sanity/GitHub topics */}
                                        <span className="px-3 py-1.5 bg-[var(--bg-tertiary)] border border-[var(--border-subtle)] rounded-lg text-sm font-medium text-[var(--text-secondary)]">GitHub API</span>
                                        <span className="px-3 py-1.5 bg-[var(--bg-tertiary)] border border-[var(--border-subtle)] rounded-lg text-sm font-medium text-[var(--text-secondary)]">Web Development</span>
                                    </div>
                                </div>

                                {/* Media Teaser Section */}
                                <div className="p-6 bg-gradient-to-r from-violet-500/5 to-cyan-500/5 border border-dashed border-violet-500/20 rounded-2xl">
                                    <h3 className="text-base font-bold text-[var(--text-primary)] mb-2 flex items-center gap-2">
                                        <span className="text-xl">📸</span> Visual Documentation
                                    </h3>
                                    <p className="text-sm text-[var(--text-tertiary)] italic">
                                        I am currently preparing high-quality screenshots and video walkthroughs for this project. They will appear here once ready.
                                    </p>
                                </div>

                                {/* CTAs */}
                                <div className="flex flex-col sm:flex-row gap-4 pt-4 pb-8">
                                    <a
                                        href={project.githubUrl}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex-1 flex items-center justify-center gap-2 px-8 py-4 bg-[var(--text-primary)] text-[var(--bg-primary)] font-bold rounded-2xl hover:opacity-90 transition-opacity"
                                    >
                                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                            <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                                        </svg>
                                        View on GitHub
                                    </a>
                                    <button
                                        onClick={onClose}
                                        className="flex-1 px-8 py-4 bg-[var(--bg-tertiary)] text-[var(--text-primary)] font-bold rounded-2xl border border-[var(--border-subtle)] hover:bg-[var(--bg-card-hover)] transition-colors"
                                    >
                                        Close Details
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>
        </AnimatePresence>
    );
}
