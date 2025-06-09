import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  IconButton,
  Divider,
  Link,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { useTranslation } from 'react-i18next';
import Global from '../../global/global';

interface AboutModalProps {
  open: boolean;
  onClose: () => void;
}

interface ProjectLink {
  name: string;
  url: string;
  icon?: string;
}

interface SocialLink {
  name: string;
  url: string;
  icon: string;
}

// Fix Issue 2: Use function declaration instead of const
function AboutModal({ open, onClose }: AboutModalProps) {
  const { t } = useTranslation();

  const projectLinks: ProjectLink[] = [
    {
      name: t('aboutModal.officialWebsite'),
      url: Global.APP_WEBSITE,
    },
    {
      name: t('aboutModal.githubRepository'),
      url: Global.GITHUB_REPO,
    },
    {
      name: t('aboutModal.documentation'),
      url: Global.DOCS_URL,
    },
  ];

  const socialLinks: SocialLink[] = [
    {
      name: t('aboutModal.twitter'),
      url: 'https://twitter.com/AntonioMrtz',
      icon: '🐦',
    },
    {
      name: t('aboutModal.linkedin'),
      url: 'https://linkedin.com/in/AntonioMrtz',
      icon: '💼',
    },
    {
      name: t('aboutModal.email'),
      url: 'mailto:contact@antoniomrtz.com',
      icon: '✉️',
    },
  ];

  const handleLinkClick = (url: string) => {
    window.open(url, '_blank');
  };

  const handleStarClick = () => {
    window.open(Global.GITHUB_REPO, '_blank');
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="sm"
      fullWidth
      aria-labelledby="about-dialog-title"
    >
      <DialogTitle id="about-dialog-title">
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">{t('aboutModal.title')}</Typography>
          <IconButton
            aria-label="Close about dialog"
            onClick={onClose}
            size="small"
          >
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>

      <DialogContent>
        <Box sx={{ py: 2 }}>
          {/* Version Info */}
          <Typography variant="body1" gutterBottom>
            {t('aboutModal.version', { version: Global.APPVERSION })}
          </Typography>

          <Divider sx={{ my: 2 }} />

          {/* Project Links */}
          <Typography variant="h6" gutterBottom>
            {t('aboutModal.projectLinks')}
          </Typography>
          <Box sx={{ mb: 2 }}>
            {/* Fix Issue 3: Use unique identifiers instead of array index as key */}
            {projectLinks.map((link) => (
              <Button
                key={link.name} // Use name as unique key instead of index
                variant="outlined"
                onClick={() => handleLinkClick(link.url)}
                sx={{ mr: 1, mb: 1 }}
                size="small"
              >
                {link.name}
              </Button>
            ))}
          </Box>

          <Divider sx={{ my: 2 }} />

          {/* Developer Info */}
          <Typography variant="h6" gutterBottom>
            {t('aboutModal.createdBy')}
          </Typography>
          <Typography variant="body2" gutterBottom>
            <Link
              href="https://github.com/AntonioMrtz"
              target="_blank"
              rel="noopener noreferrer"
            >
              AntonioMrtz
            </Link>
          </Typography>

          <Typography variant="body2" gutterBottom>
            {t('aboutModal.connectDeveloper')}
          </Typography>

          <Box sx={{ mb: 2 }}>
            {/* Fix Issue 3: Use unique identifiers instead of array index as key */}
            {socialLinks.map((social) => (
              <Button
                key={social.name} // Use name as unique key instead of index
                variant="text"
                onClick={() => handleLinkClick(social.url)}
                sx={{ mr: 1, mb: 1 }}
                size="small"
                startIcon={<span>{social.icon}</span>}
              >
                {social.name}
              </Button>
            ))}
          </Box>

          <Divider sx={{ my: 2 }} />

          {/* Support Text */}
          <Typography variant="body2" gutterBottom>
            {t('aboutModal.supportText')}
          </Typography>
        </Box>
      </DialogContent>

      <DialogActions>
        <Button variant="contained" onClick={handleStarClick} color="primary">
          {t('aboutModal.starButton')}
        </Button>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
}

export default AboutModal;
