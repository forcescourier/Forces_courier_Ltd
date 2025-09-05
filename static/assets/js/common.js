/* Common JavaScript Functions - Courier Management System */
/* Shared functionality used across multiple pages */

(function($) {
    'use strict';

    // Namespace for common functions
    window.CourierApp = window.CourierApp || {};

    /**
     * Enhanced toast notifications with consistent styling
     */
    CourierApp.showToast = function(message, type, duration) {
        type = type || 'info';
        duration = duration || 3000;

        var alertClass = type === 'success' ? 'alert-success' : 
                        type === 'error' ? 'alert-danger' : 
                        type === 'warning' ? 'alert-warning' : 'alert-info';
        
        var iconClass = type === 'success' ? 'fa-check-circle' : 
                       type === 'error' ? 'fa-exclamation-circle' : 
                       type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';
        
        var toast = `<div class="alert ${alertClass} alert-dismissible fade show position-fixed" 
                         style="top: 20px; right: 20px; z-index: 9999; min-width: 300px; max-width: 500px;">
                        <i class="fas ${iconClass} mr-2"></i>
                        ${message}
                        <button type="button" class="close" data-dismiss="alert">
                            <span>&times;</span>
                        </button>
                     </div>`;
        
        $('body').append(toast);
        
        // Auto remove after specified duration
        setTimeout(function() {
            $('.alert').fadeOut(500, function() {
                $(this).remove();
            });
        }, duration);
    };

    /**
     * Initialize enhanced DataTables with consistent settings
     */
    CourierApp.initDataTable = function(selector, options) {
        var defaultOptions = {
            pageLength: 15,
            responsive: true,
            language: {
                search: "Search:",
                lengthMenu: "Show _MENU_ entries",
                info: "Showing _START_ to _END_ of _TOTAL_ entries",
                paginate: {
                    first: "First",
                    last: "Last",
                    next: "Next",
                    previous: "Previous"
                }
            },
            dom: '<"row"<"col-md-6"l><"col-md-6"f>>rtip',
            columnDefs: [
                { targets: 'no-sort', orderable: false }
            ],
            drawCallback: function() {
                // Apply theme styling after table draw
                CourierApp.applyTableStyling();
            }
        };

        options = $.extend({}, defaultOptions, options || {});
        return $(selector).DataTable(options);
    };

    /**
     * Apply consistent table styling
     */
    CourierApp.applyTableStyling = function() {
        // Add enhanced classes to tables
        $('.dataTable').addClass('data-table');
        
        // Style pagination
        $('.dataTables_paginate .paginate_button').each(function() {
            if (!$(this).hasClass('current') && !$(this).hasClass('disabled')) {
                $(this).removeClass('btn-primary').addClass('btn-outline-primary');
            }
        });
    };

    /**
     * Enhanced form validation with consistent styling
     */
    CourierApp.validateForm = function(formSelector, rules, messages) {
        return $(formSelector).validate({
            rules: rules,
            messages: messages,
            errorClass: 'is-invalid',
            validClass: 'is-valid',
            errorPlacement: function(error, element) {
                error.addClass('invalid-feedback');
                if (element.parent().hasClass('input-group')) {
                    element.parent().after(error);
                } else {
                    element.after(error);
                }
            },
            highlight: function(element) {
                $(element).removeClass('is-valid').addClass('is-invalid');
            },
            unhighlight: function(element) {
                $(element).removeClass('is-invalid').addClass('is-valid');
            },
            submitHandler: function(form) {
                CourierApp.showToast('Form validation passed. Processing...', 'success');
                return true;
            }
        });
    };

    /**
     * Bulk selection functionality for tables
     */
    CourierApp.initBulkSelection = function(tableSelector, checkboxSelector) {
        // Select all functionality
        $(document).on('change', '.select-all-checkbox', function() {
            var isChecked = $(this).prop('checked');
            $(tableSelector + ' ' + checkboxSelector).prop('checked', isChecked);
            CourierApp.updateBulkActionState(tableSelector, checkboxSelector);
        });

        // Individual checkbox change
        $(document).on('change', tableSelector + ' ' + checkboxSelector, function() {
            var totalCheckboxes = $(tableSelector + ' ' + checkboxSelector).length;
            var checkedCheckboxes = $(tableSelector + ' ' + checkboxSelector + ':checked').length;
            
            $('.select-all-checkbox').prop('checked', totalCheckboxes === checkedCheckboxes);
            CourierApp.updateBulkActionState(tableSelector, checkboxSelector);
        });
    };

    /**
     * Update bulk action form state based on selections
     */
    CourierApp.updateBulkActionState = function(tableSelector, checkboxSelector) {
        var checkedCount = $(tableSelector + ' ' + checkboxSelector + ':checked').length;
        var bulkForm = $('.bulk-action-form');
        
        if (checkedCount > 0) {
            bulkForm.removeClass('opacity-60').css('pointer-events', 'auto');
            bulkForm.find('.selected-count').text(checkedCount);
            bulkForm.addClass('bg-light');
        } else {
            bulkForm.addClass('opacity-60').css('pointer-events', 'none');
            bulkForm.find('.selected-count').text('0');
            bulkForm.removeClass('bg-light');
        }
    };

    /**
     * Enhanced modal functionality
     */
    CourierApp.showModal = function(modalId, title, content, buttons) {
        var modal = $('#' + modalId);
        if (modal.length === 0) {
            // Create modal if it doesn't exist
            modal = CourierApp.createModal(modalId, title, content, buttons);
        } else {
            // Update existing modal
            modal.find('.modal-title').text(title);
            modal.find('.modal-body').html(content);
            if (buttons) {
                modal.find('.modal-footer').html(buttons);
            }
        }
        modal.modal('show');
        return modal;
    };

    /**
     * Create a new modal dynamically
     */
    CourierApp.createModal = function(modalId, title, content, buttons) {
        var modalHtml = `
            <div class="modal fade" id="${modalId}" tabindex="-1" role="dialog">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="close" data-dismiss="modal">
                                <span>&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            ${content}
                        </div>
                        <div class="modal-footer">
                            ${buttons || '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'}
                        </div>
                    </div>
                </div>
            </div>
        `;
        $('body').append(modalHtml);
        return $('#' + modalId);
    };

    /**
     * Confirm dialog with consistent styling
     */
    CourierApp.confirm = function(message, title, callback) {
        title = title || 'Confirmation';
        var modalId = 'confirmModal';
        var buttons = `
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary" id="confirmButton">Confirm</button>
        `;
        
        var modal = CourierApp.showModal(modalId, title, message, buttons);
        
        modal.find('#confirmButton').off('click').on('click', function() {
            modal.modal('hide');
            if (callback && typeof callback === 'function') {
                callback(true);
            }
        });
        
        modal.off('hidden.bs.modal').on('hidden.bs.modal', function() {
            if (callback && typeof callback === 'function') {
                // Only call with false if not already called with true
                var alreadyCalled = $(this).data('already-called');
                if (!alreadyCalled) {
                    callback(false);
                }
            }
            $(this).removeData('already-called');
        });
        
        modal.find('#confirmButton').on('click', function() {
            modal.data('already-called', true);
        });
    };

    /**
     * Loading state management
     */
    CourierApp.showLoading = function(element, text) {
        text = text || 'Loading...';
        var $element = $(element);
        var originalText = $element.data('original-text') || $element.html();
        $element.data('original-text', originalText);
        
        $element.prop('disabled', true)
                .html('<i class="fas fa-spinner fa-spin mr-2"></i>' + text);
    };

    CourierApp.hideLoading = function(element) {
        var $element = $(element);
        var originalText = $element.data('original-text');
        if (originalText) {
            $element.prop('disabled', false).html(originalText);
        }
    };

    /**
     * Format currency with consistent formatting
     */
    CourierApp.formatCurrency = function(amount, currency) {
        currency = currency || 'BDT';
        if (typeof amount === 'string') {
            amount = parseFloat(amount.replace(/[^\d.-]/g, ''));
        }
        return currency + ' ' + amount.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    };

    /**
     * Format date with consistent formatting
     */
    CourierApp.formatDate = function(date, format) {
        format = format || 'DD/MM/YYYY';
        if (typeof date === 'string') {
            date = new Date(date);
        }
        return moment(date).format(format);
    };

    /**
     * Debounce function for search inputs
     */
    CourierApp.debounce = function(func, wait, immediate) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            var later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    };

    /**
     * Initialize search functionality with debounce
     */
    CourierApp.initSearch = function(inputSelector, searchFunction, delay) {
        delay = delay || 300;
        $(document).on('input', inputSelector, CourierApp.debounce(function() {
            var query = $(this).val();
            if (searchFunction && typeof searchFunction === 'function') {
                searchFunction(query);
            }
        }, delay));
    };

    /**
     * Copy to clipboard functionality
     */
    CourierApp.copyToClipboard = function(text, successMessage) {
        successMessage = successMessage || 'Copied to clipboard!';
        
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(function() {
                CourierApp.showToast(successMessage, 'success');
            }).catch(function(err) {
                console.error('Failed to copy: ', err);
                CourierApp.fallbackCopyTextToClipboard(text, successMessage);
            });
        } else {
            CourierApp.fallbackCopyTextToClipboard(text, successMessage);
        }
    };

    /**
     * Fallback copy to clipboard for older browsers
     */
    CourierApp.fallbackCopyTextToClipboard = function(text, successMessage) {
        var textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.top = "-1000px";
        textArea.style.left = "-1000px";
        
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            CourierApp.showToast(successMessage, 'success');
        } catch (err) {
            console.error('Fallback: Oops, unable to copy', err);
            CourierApp.showToast('Failed to copy to clipboard', 'error');
        }
        
        document.body.removeChild(textArea);
    };

    /**
     * Initialize common functionality when document is ready
     */
    $(document).ready(function() {
        // Initialize tooltips
        $('[data-toggle="tooltip"]').tooltip();
        
        // Initialize popovers
        $('[data-toggle="popover"]').popover();
        
        // Add enhanced classes to existing elements
        $('.form-control').addClass('form-control-enhanced');
        $('.btn-primary').addClass('btn-enhanced');
        $('.card').addClass('card-enhanced');
        
        // Initialize copy to clipboard buttons
        $(document).on('click', '[data-copy]', function() {
            var text = $(this).data('copy');
            CourierApp.copyToClipboard(text);
        });
        
        // Enhance form controls focus behavior
        $('.form-control-enhanced').on('focus', function() {
            $(this).parent().addClass('focused');
        }).on('blur', function() {
            $(this).parent().removeClass('focused');
        });
        
        // Close dropdown menus when clicking outside
        $(document).on('click', function(e) {
            var statusMenu = $('#statusMenu');
            var riderMenu = $('#riderMenu');
            
            if (statusMenu.length && !$(e.target).closest('#statusBtn, #statusMenu').length) {
                statusMenu.hide();
            }
            
            if (riderMenu.length && !$(e.target).closest('#riderBtn, #riderMenu').length) {
                riderMenu.hide();
            }
        });
    });

    /**
     * Toggle select all functionality for tables
     */
    CourierApp.toggleSelectAll = function(tableSelector, checkboxSelector) {
        var selectAllCheckbox = $(tableSelector).find('.select-all-checkbox, #selectAll').first();
        var checkboxes = $(tableSelector).find(checkboxSelector);
        var isChecked = selectAllCheckbox.prop('checked');
        
        checkboxes.prop('checked', isChecked);
        CourierApp.updateBulkActionState(tableSelector, checkboxSelector);
    };

    /**
     * Toggle dropdown menu functionality
     */
    CourierApp.toggleDropdownMenu = function(showMenuId, hideMenuId) {
        var showMenu = document.getElementById(showMenuId);
        var hideMenu = document.getElementById(hideMenuId);
        
        // Hide the other menu first
        if (hideMenu) {
            hideMenu.style.display = 'none';
        }
        
        // Toggle the target menu
        if (showMenu) {
            if (showMenu.style.display === 'none' || showMenu.style.display === '') {
                showMenu.style.display = 'block';
            } else {
                showMenu.style.display = 'none';
            }
        }
    };

    /**
     * Select bulk status for batch operations
     */
    CourierApp.selectBulkStatus = function(status, buttonId) {
        window.selectedStatus = status;
        var statusBtn = document.getElementById(buttonId);
        
        var statusLabels = {
            'pending': '⏳ Pending',
            'pickup': '📦 Pickup Assigned', 
            'transit': '🚚 In Transit',
            'delivery': '🚛 Out for Delivery',
            'delivered': '✅ Delivered',
            'returned': '↩️ Returned'
        };
        
        if (statusBtn && statusLabels[status]) {
            statusBtn.innerHTML = '<i class="fas fa-tasks"></i> ' + statusLabels[status];
            statusBtn.className = 'btn btn-info btn-sm';
            
            // Hide menu
            var statusMenu = document.getElementById('statusMenu');
            if (statusMenu) {
                statusMenu.style.display = 'none';
            }
            
            CourierApp.showToast('Status selected: ' + statusLabels[status], 'info', 1500);
        }
    };

    /**
     * Select bulk rider for batch operations
     */
    CourierApp.selectBulkRider = function(rider, buttonId) {
        window.selectedRider = rider;
        var riderBtn = document.getElementById(buttonId);
        
        var riderLabels = {
            'rider1': '👤 Ahmed Rahman',
            'rider2': '👤 Karim Uddin',
            'rider3': '👤 Nasir Mahmud',
            'rider4': '👤 Salma Begum',
            'rider5': '👤 Fahim Hassan'
        };
        
        if (riderBtn && riderLabels[rider]) {
            riderBtn.innerHTML = '<i class="fas fa-user"></i> ' + riderLabels[rider];
            riderBtn.className = 'btn btn-warning btn-sm';
            
            // Hide menu
            var riderMenu = document.getElementById('riderMenu');
            if (riderMenu) {
                riderMenu.style.display = 'none';
            }
            
            CourierApp.showToast('Rider selected: ' + riderLabels[rider], 'info', 1500);
        }
    };

    /**
     * Submit bulk action for selected items
     */
    CourierApp.submitBulkAction = function(checkboxSelector) {
        var selectedItems = $(checkboxSelector + ':checked');
        
        if (selectedItems.length === 0) {
            CourierApp.showToast('Please select at least one item', 'warning');
            return;
        }
        
        var selectedStatus = window.selectedStatus || '';
        var selectedRider = window.selectedRider || '';
        
        if (!selectedStatus && !selectedRider) {
            CourierApp.showToast('Please select at least one action (Status or Rider)', 'warning');
            return;
        }
        
        var message = `Processing ${selectedItems.length} item(s)...`;
        CourierApp.showToast(message, 'info');
        
        // Simulate processing
        setTimeout(function() {
            var successMessage = `Successfully updated ${selectedItems.length} item(s)`;
            if (selectedStatus) successMessage += ` with status: ${selectedStatus}`;
            if (selectedRider) successMessage += ` assigned to rider: ${selectedRider}`;
            
            CourierApp.showToast(successMessage, 'success');
            
            // Reset selections
            window.selectedStatus = '';
            window.selectedRider = '';
            selectedItems.prop('checked', false);
            
            // Reset bulk action buttons
            var statusBtn = document.getElementById('statusBtn');
            var riderBtn = document.getElementById('riderBtn');
            if (statusBtn) {
                statusBtn.innerHTML = '<i class="fas fa-tasks"></i> Select Status';
                statusBtn.className = 'btn btn-outline-secondary btn-sm';
            }
            if (riderBtn) {
                riderBtn.innerHTML = '<i class="fas fa-user"></i> Select Rider';
                riderBtn.className = 'btn btn-outline-secondary btn-sm';
            }
            
            // Update bulk action state
            CourierApp.updateBulkActionState('#parcelsTable', '.parcel-checkbox');
        }, 2000);
    };

    /**
     * Initialize tooltips with consistent settings
     */
    CourierApp.initTooltips = function() {
        $('[title], [data-toggle="tooltip"]').tooltip({
            placement: 'top',
            trigger: 'hover',
            delay: { show: 500, hide: 100 }
        });
    };

})(jQuery);