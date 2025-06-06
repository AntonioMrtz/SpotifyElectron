"use client"

import type React from "react"
import { Dialog, DialogTitle, DialogContent, IconButton, Typography, Box, Chip, Button, Avatar } from "@mui/material"
import {
  Close as CloseIcon,
  MusicNote as MusicIcon,
  GitHub as GitHubIcon,
  Language as WebIcon,
  MenuBook as DocsIcon,
  Person as PersonIcon,
  Star as StarIcon,
} from "@mui/icons-material"
import { t } from "i18next"
import Global from "global/global"
import styles from "./AboutModal.module.css"

interface AboutModalProps {
  open: boolean
  onClose: () => void
}

const AboutModal: React.FC<AboutModalProps> = ({ open, onClose }) => {
  // Get version safely with fallback
  let APP_VERSION = "v1.0.0"
  try {
    APP_VERSION = Global.APPVERSION || "v1.0.0"
  } catch (error) {
    APP_VERSION = "v1.0.0"
  }

  const GITHUB_REPO = Global.repositoryUrl || "https://github.com/AntonioMrtz/SpotifyElectron"
  const APP_WEBSITE = "https://your-website.com"
  const DOCS_URL = "https://your-docs.com"

  const handleExternalLink = (url: string) => {
    window.open(url, "_blank")
  }

  const socialLinks = [
    {
      name: "Twitter",
      url: "https://twitter.com/AntonioMrtz",
      icon: "🐦",
    },
    {
      name: "LinkedIn",
      url: "https://linkedin.com/in/antoniomrtz",
      icon: "💼",
    },
    {
      name: "Email",
      url: "mailto:contact@antoniomrtz.com",
      icon: "✉️",
    },
  ]

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="sm"
      fullWidth
      className={styles.modal}
      BackdropProps={{
        className: styles.modalBackdrop,
      }}
      PaperProps={{
        className: styles.modalPaper,
      }}
    >
      {/* Header */}
      <DialogTitle className={styles.modalHeader}>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <Box sx={{ display: "flex", alignItems: "center" }}>
            <MusicIcon className={styles.appIcon} />
            <Typography className={styles.title}>{t("aboutModal.title") || "Spotify Electron"}</Typography>
          </Box>
          <IconButton onClick={onClose} className={styles.closeButton} aria-label="Close about dialog">
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>

      <DialogContent className={styles.modalContent}>
        {/* Version Section */}
        <Box sx={{ textAlign: "center", mb: 3 }}>
          <Chip
            label={t("aboutModal.version", { version: APP_VERSION }) || `Version ${APP_VERSION}`}
            className={styles.versionChip}
          />
        </Box>

        {/* Links Section */}
        <Box className={`${styles.section} ${styles.sectionFirst}`}>
          <Typography className={styles.sectionTitle} sx={{ mb: 2 }}>
            {t("aboutModal.projectLinks") || "Project Links"}
          </Typography>

          <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
            <Button
              startIcon={<WebIcon className={styles.projectLinkIcon} />}
              onClick={() => handleExternalLink(APP_WEBSITE)}
              className={styles.linkButton}
            >
              {t("aboutModal.officialWebsite") || "Official Website"}
            </Button>

            <Button
              startIcon={<GitHubIcon className={styles.projectLinkIcon} />}
              onClick={() => handleExternalLink(GITHUB_REPO)}
              className={styles.linkButton}
            >
              {t("aboutModal.githubRepository") || "GitHub Repository"}
            </Button>

            <Button
              startIcon={<DocsIcon className={styles.projectLinkIcon} />}
              onClick={() => handleExternalLink(DOCS_URL)}
              className={styles.linkButton}
            >
              {t("aboutModal.documentation") || "Documentation"}
            </Button>
          </Box>
        </Box>

        {/* Developer Section */}
        <Box className={styles.section}>
          <Typography className={styles.sectionTitle} sx={{ mb: 2 }}>
            <PersonIcon className={styles.appIcon} sx={{ mr: 1 }} />
            {t("aboutModal.createdBy") || "Created by"}
          </Typography>

          <Box className={styles.developerSection}>
            <Avatar className={styles.developerAvatar}>AM</Avatar>
            <Box sx={{ flex: 1 }}>
              <Typography className={styles.primaryText}>AntonioMrtz</Typography>
              <Typography className={styles.secondaryText} sx={{ mb: 1 }}>
                {t("aboutModal.connectDeveloper") || "Connect with the developer"}
              </Typography>
            </Box>
          </Box>

          <Box className={styles.socialLinksContainer}>
            {socialLinks.map((social) => (
              <Button
                key={social.name}
                size="small"
                onClick={() => handleExternalLink(social.url)}
                className={styles.socialButton}
              >
                {social.icon} {social.name}
              </Button>
            ))}
          </Box>
        </Box>

        {/* Star Section */}
        <Box className={styles.ctaSection}>
          <Typography className={styles.secondaryText} sx={{ mb: 2 }}>
            {t("aboutModal.supportText") || "If you like this project, consider giving it a star!"}
          </Typography>

          <Button
            variant="contained"
            startIcon={<StarIcon />}
            onClick={() => handleExternalLink(GITHUB_REPO)}
            className={styles.starButton}
          >
            {t("aboutModal.starButton") || "Star on GitHub"}
          </Button>
        </Box>
      </DialogContent>
    </Dialog>
  )
}

export default AboutModal
